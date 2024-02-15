import itertools
import numpy as np
from scipy import constants, interpolate

from idstools.compute.equilibrium import EquilibriumCompute
from idstools.compute.waves import WavesCompute
from idstools.compute.common import getClosestOfGivenValueFromArray


class EcStrayCompute:
    def __init__(
        self, equilibriumIds: object, coreProfilesIds: object, wavesIds: object
    ):
        self.equilibriumIds = equilibriumIds
        self.coreProfilesIds = coreProfilesIds
        self.wavesIds = wavesIds

        self.equilibriumCompute = EquilibriumCompute(equilibriumIds)
        # self.coreProfilesCompute = coreProfilesIds
        self.wavesCompute = WavesCompute(wavesIds)

    def getResonanceLayer(
        self, timeIndexWaves: int = 0, timeIndexEquilibrium: int = 0, nHarm=None
    ):
        """This function calculates and returns a dictionary (Resonance Layer) containing r and z values corresponding to the resonance points based on the provided nHarm values, BResonance, and bTotal arrays.

        Args:
            timeIndexWaves (int): time index for waves, default is 0
            timeIndexEquilibrium (int): time index of equilibrium, default is 0
            nHarm (list, optional):  integer values that represent the order or index of harmonics in a series. Defaults to [1, 2, 3, 4].

        Returns:
            dict: returns dictionary of  resonance layer for specific harmonics

        Examples:
            .. code-block:: python

                import imas
                # add necessary imports
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                coreProfilesIds = connection.get('waves')
                wavesIds = connection.get('core_profiles')

                ecstrayCompute = EcStrayCompute(equilibriumIds, coreProfilesIds, wavesIds)

                resonance_layer = ecstrayCompute.getResonanceLayer()

                {0: {'r': [5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375,
                5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375, 5.4375],
                'z': [-6.0, -5.90625, -5.8125, -5.71875, -5.625, -5.53125, -5.4375, -5.34375, -5.25, -5.15625,
                5.71875, 5.8125, 5.90625, 6.0]}, 1: {'r': [], 'z': []}, 2: {'r': [], 'z': []}, 3: {'r': [], 'z': []}}

        """
        if nHarm is None:
            nHarm = [1, 2, 3, 4]
        BResonance = self.wavesCompute.getBResonance(
            timeIndex=timeIndexWaves, harmonicFrequencies=nHarm
        )
        profile2dIndex, bTotal = self.equilibriumCompute.getBTotal(timeIndexEquilibrium)
        if profile2dIndex != -99:
            r = (
                self.equilibriumCompute.ids.time_slice[timeIndexEquilibrium]
                .profiles_2d[profile2dIndex]
                .grid.dim1
            )
            z = (
                self.equilibriumCompute.ids.time_slice[timeIndexEquilibrium]
                .profiles_2d[profile2dIndex]
                .grid.dim2
            )

        [nr, nz] = np.shape(bTotal)
        b_err = 10 / nr

        resonanceLayer = {}
        for indexHarm in range(len(nHarm)):
            resonanceLayer[indexHarm] = {"r": [], "z": []}
            for iz in range(nz):
                [ir, rloc] = getClosestOfGivenValueFromArray(
                    bTotal[:, iz], BResonance[indexHarm]
                )
                if np.abs(bTotal[ir, iz] - BResonance[indexHarm]) < b_err:
                    resonanceLayer[indexHarm]["r"].append(r[ir])
                    resonanceLayer[indexHarm]["z"].append(z[iz])

        return {"profile2dIndex": profile2dIndex, "resonanceLayer": resonanceLayer}

    def getCutoffLayer(
        self,
        timeIndexWaves: int = 0,
        timeIndexCoreProfiles: int = 0,
        timeIndexEquilibrium: int = 0,
    ):
        """The cutoff layer is a region in a plasma where certain frequencies or modes of wave propagation are prevented from propagating or transmitting due to the plasma's properties.

        Args:
            timeIndexWaves (int, optional): time index for waves. Defaults to 0.
            timeIndexCoreProfiles (int, optional): time index for core_profiles. Defaults to 0.
            timeIndexEquilibrium (int, optional): time index for equilibrium. Defaults to 0.

        Returns:
            dict: cut off layer in dictionary format

        Notes:

            ω_R = √[(eB/m_e/2)^2 + n_e * e^2/(ε_0 * m_e)] + eB/m_e/2

            electron cyclotron frequency in plasma physics. It is denoted by ω_R and can be calculated using the equation

            where:

            - ``ω_R`` is the electron cyclotron frequency
            - ``e`` is the elementary charge
            - ``B`` is the magnetic field strength
            - ``m_e`` is the mass of an electron
            - ``n_e`` is the electron number density
            - ``ε_0`` is the vacuum permittivity

        Examples:
            .. code-block:: python

                import imas

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                connection.open()
                equilibriumIds = connection.get('equilibrium')
                coreProfilesIds = connection.get('waves')
                wavesIds = connection.get('core_profiles')

                ecStrayCompute = EcStrayCompute(equilibriumIds, coreProfilesIds, wavesIds)

                cut_off_layer = ecStrayCompute.getCutoffLayer()

                {'r': [5.625, 5.4375, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125,
                5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.53125, 5.4375],
                'z': [-2.15625, -2.0625, -1.96875, -1.875, -1.78125, -1.6875, -1.59375, -1.5, -1.40625, -1.3125, -1.21875,
                1.03125, 1.125, 1.21875, 1.3125, 1.40625, 1.5, 1.59375, 1.6875, 1.78125, 1.875, 1.96875, 2.0625, 2.15625]}

        """
        # wavecompute = WavesCompute(self.wavesIds)
        omega_ec = self.wavesCompute.getOmegaEC(timeIndexWaves)

        # Find (R,Z) rectangular grid of B-field
        # eqcomputeobj = EquilibriumCompute(self.equilibriumIds)
        profile2dIndex, bTotal = self.equilibriumCompute.getBTotal(timeIndexEquilibrium)

        # B(R,Z) evaluation
        r = (
            self.equilibriumIds.time_slice[timeIndexEquilibrium]
            .profiles_2d[profile2dIndex]
            .grid.dim1
        )
        z = (
            self.equilibriumIds.time_slice[timeIndexEquilibrium]
            .profiles_2d[profile2dIndex]
            .grid.dim2
        )

        # Ne(psi) in core_profiles IDS
        rho1d_cp = self.coreProfilesIds.profiles_1d[
            timeIndexCoreProfiles
        ].grid.rho_tor_norm
        psi1d_cp = (
            self.coreProfilesIds.profiles_1d[timeIndexCoreProfiles].grid.psi
            - self.coreProfilesIds.profiles_1d[timeIndexCoreProfiles].grid.psi[-1]
        ) / (
            self.coreProfilesIds.profiles_1d[timeIndexCoreProfiles].grid.psi[0]
            - self.coreProfilesIds.profiles_1d[timeIndexCoreProfiles].grid.psi[-1]
        )
        ne_cp = self.coreProfilesIds.profiles_1d[
            timeIndexCoreProfiles
        ].electrons.density

        # Ne(psi) interpolated over equilibrium IDS
        rho1d_eq = self.equilibriumIds.time_slice[
            timeIndexEquilibrium
        ].profiles_1d.rho_tor_norm
        psi1d_eq = (
            self.equilibriumIds.time_slice[timeIndexEquilibrium].profiles_1d.psi
            - self.equilibriumIds.time_slice[timeIndexEquilibrium].profiles_1d.psi[-1]
        ) / (
            self.equilibriumIds.time_slice[timeIndexEquilibrium].profiles_1d.psi[0]
            - self.equilibriumIds.time_slice[timeIndexEquilibrium].profiles_1d.psi[-1]
        )
        ne_eq = np.zeros(len(psi1d_eq))
        ne_interp = interpolate.interp1d(psi1d_cp, ne_cp, kind="linear")
        for i in range(len(psi1d_eq)):
            ne_eq[i] = float(ne_interp(psi1d_eq[i]))

        # Ne(R,Z) deduced for each point over B(R,Z) in equilibrium IDS
        psi1d_eq = self.equilibriumIds.time_slice[timeIndexEquilibrium].profiles_1d.psi
        psi2d_eq = (
            self.equilibriumIds.time_slice[timeIndexEquilibrium]
            .profiles_2d[profile2dIndex]
            .psi
        )
        ne_from_psi = interpolate.interp1d(psi1d_eq, ne_eq, kind="linear")
        ne2d_eq = np.zeros(np.shape(psi2d_eq))
        omegaR = np.zeros(np.shape(psi2d_eq))
        for ir, iz in itertools.product(range(len(r)), range(len(z))):
            try:  # Inside LCFS
                ne2d_eq[ir, iz] = ne_from_psi(psi2d_eq[ir, iz])
                # omega_R = sqrt[(eB/m_e/2)**2 + n_e *e**2/(epsilon_0*m_e)] + eB/m_e/2
                omegaR[ir, iz] = np.sqrt(
                    (constants.e * bTotal[ir, iz] / (2 * constants.m_e)) ** 2
                    + ne2d_eq[ir, iz]
                    * constants.e**2
                    / (constants.epsilon_0 * constants.m_e)
                ) + constants.e * bTotal[ir, iz] / (2 * constants.m_e)
            except Exception:  # Not defined outside LCFS
                ne2d_eq[ir, iz] = -1  # np.NaN
                omegaR[ir, iz] = -1  # np.NaN

        # Find (R,Z) where omega_R = omega_EC (within the tolerance omega_err)
        [nr, nz] = np.shape(omegaR)
        omegaErr = 100 / nr

        cutoffLayer = {"r": [], "z": []}
        for iz in range(nz):
            [ir, rloc] = getClosestOfGivenValueFromArray(omegaR[:, iz], omega_ec)
            if np.abs((omegaR[ir, iz] - omega_ec) / omegaR[ir, iz]) < omegaErr:
                cutoffLayer["r"].append(r[ir])
                cutoffLayer["z"].append(z[iz])

        return cutoffLayer
