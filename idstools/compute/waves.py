""" 
This module provides compute functions and classes for waves ids data

`more about waves ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/waves.html>`_.

"""

import functools
import numpy as np


class WavesCompute:
    """This class provides compute functions for waves ids"""

    def __init__(self, ids):
        """Initialization WavesCompute object.

        Args:
            ids : waves ids object
        """
        self.ids = ids

    def getBResonance(
        self,
        coherentWaveIndex: int = 0,
        timeIndex: int = 0,
        harmonicFrequencies: list = None,
    ):
        """
        This function calculates the B-resonance (magnetic field) for a given coherent wave index, time index, and list of harmonic frequencies.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which we want to calculate the B resonance. Defaults to 0
            timeIndex (int): The index of the time step for which the bResonance is being calculated. Defaults to 0
            harmonicFrequencies (list): A list of integers representing the harmonic frequencies for which the B-resonance values are to be calculated. If this parameter is not provided, the function uses the default values of [1, 2, 3, 4].

        Returns:
            A list of values for the magnetic field resonance frequencies for the given coherent wave index, time index, and harmonic frequencies. The length of the list is equal to the length of the input harmonic frequencies list.


        Notes:
            .. math:: BResonance = \ 2*pi*ecfrequency*9.1e^-31/1.6e^-19/HarmonicFrequency

            Here harmonicFrequency is any value from [1,2,3,4]

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBResonance())

                [6.0750547938792625, 3.0375273969396313, 2.025018264626421, 1.5187636984698156]
        """
        if harmonicFrequencies is None:
            harmonicFrequencies = [1, 2, 3, 4]
        ecFrequency = (
            self.ids.coherent_wave[coherentWaveIndex]
            .global_quantities[timeIndex]
            .frequency
        )
        bResonance = [0] * len(harmonicFrequencies)
        for harmonicFrequencyIndex in range(len(harmonicFrequencies)):
            bResonance[harmonicFrequencyIndex] = (
                2
                * np.pi
                * ecFrequency
                * 9.1e-31
                / 1.6e-19
                / harmonicFrequencies[harmonicFrequencyIndex]
            )
        return bResonance

    def getBeamArray(self):
        """
        This function returns an array of beam indices based on the number of coherent waves.

        Returns:
            a numpy array of equally spaced values from 0 to nbeam-1, where nbeam is the length of the list `waves.coherent_wave`. This array represents the indices of the beams.

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBeamArray())

                [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
        """
        nBeam = len(self.ids.coherent_wave)
        return np.linspace(0, nBeam - 1, nBeam)

    def getOmegaEC(self, coherentWaveIndex: int = 0, timeIndex: int = 0) -> float:
        """
        This function returns the angular frequency of a coherent wave at a specific time index.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which the angular frequency needs to be calculated. Defaults to 0
            timeIndex (int): The time index parameter is used to specify the time step for which the frequency of the coherent wave is to be retrieved. Defaults to 0

        Returns:
            The value of the angular frequency (in radians per second) of a coherent wave at a specific time index. The value is calculated using the frequency of the coherent wave at the given time index and multiplying it by 2*pi.

        Notes:
            .. math:: OmegaEC = \ 2*pi*frequency

        Example:
            .. code-block:: python


                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getOmegaEC())

                1068141502220.5297
        """
        return (
            2
            * np.pi
            * self.ids.coherent_wave[coherentWaveIndex]
            .global_quantities[timeIndex]
            .frequency
        )

    @functools.lru_cache(maxsize=128)
    def getActiveBeams(self, beamTracingTimeIndex: int = 0):
        """
        This function returns a dictionary of active beams with their respective properties.

        Args:
            beamTracingTimeIndex (int): The parameter `beamTracingTimeIndex` is an integer that represents the index of the beam tracing time. Defaults to 0

        Returns:
            Dictionary called `activeBeams` which contains information about each beam in `waves.coherent_wave`. The dictionary has keys for each beam index and the values are  dictionaries containing the total number of beams and boolean indicating whether the beam is active or not. The function determines if a beam is active by checking if any of its rays have initial power greater than 0.

        Example:
            .. code-block:: python


                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getActiveBeams())

                {0: {'active': True, 'total_beams': 5},
                1: {'active': True, 'total_beams': 5},
                2: {'active': True, 'total_beams': 5},
                3: {'active': True, 'total_beams': 5},
                4: {'active': True, 'total_beams': 5},
                5: {'active': True, 'total_beams': 5},
                6: {'active': True, 'total_beams': 5},
                7: {'active': True, 'total_beams': 5},
                8: {'active': True, 'total_beams': 5},
                9: {'active': True, 'total_beams': 5},
                10: {'active': True, 'total_beams': 5}}
        """
        activeBeams = {}

        for beamIndex in range(len(self.ids.coherent_wave)):
            beamDict = {
                "total_beams": len(
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam
                ),
            }
            for rayIndex in range(beamDict["total_beams"]):
                if (
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam[rayIndex]
                    .power_initial
                    > 0
                ):
                    # todo: this will loop and overwrite value, is it intended?
                    beamDict["active"] = True
            activeBeams[beamIndex] = beamDict

        return activeBeams

    def getBeamTracing(self, beamTracingTimeIndex: int = 0):
        """
        This function returns a dictionary containing information about the beam tracing of a coherent wave.

        Args:
            beamTracingTimeIndex (int): The index of the time step for which to retrieve the beam tracing data. Defaults to 0

        Returns:
            a dictionary named "beam_tracing" which contains various arrays and values related to the beam tracing data. Following are the values returned by the function

            return values

                - nbeam
                - nbeam_active
                - nray
                - is_active
                - len_ray
                - x_ray
                - y_ray
                - z_ray
                - r_ray
                - phi_ray
                - central_ray_power
                - central_ray_powerpar
                - central_ray_powerperp
                - central_ray_length

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBeamTracing())

            Output

                .. code-block:: python

                    {'central_ray_length': array([[0.        , 0.01
                    'central_ray_power': array([[     0.        ,
                    'central_ray_powerpar': array([[0., 0., 0., ..., 0., 0., 0.],
                    'central_ray_powerperp': array([[0., 0., 0., ..., 0., 0., 0.],
                    'is_active': [True,
                    'len_ray': array([[1762, 1762, 1762, 1762, 1762],
                    'nbeam': 11,
                    'nbeam_active': 11,
                    'nray': 5,
                    'phi_ray': array([[[-1.49735105, -1.49767271, -1.49799498, ...,  0.
                    'r_ray': array([[[9.98118786, 9.97171675, 9.96224668, ..., 0.
                    'x_ray': array([[[ 0.73241223,  0.72851836,  0.72462449, ...,  0.
                    'y_ray': array([[[-9.95427965, -9.94506893, -9.9358582 , ...,  0.
                    'z_ray': array([[[ 1.25254314,  1.25252628,  1.25250942, ...,  0.
        """
        # TODO This is long function but due to the data retrival in for loop it makes easy to continue in the same function
        # Count number of active beams and their number of rays
        activeBeamsDict = self.getActiveBeams(beamTracingTimeIndex)
        totalWaves = len(activeBeamsDict.keys())
        activeBeamsArray = [data["active"] for _, data in activeBeamsDict.items()]
        totalBeamsArray = [data["total_beams"] for _, data in activeBeamsDict.items()]

        # We assume the same number of rays for each beam, to simplify (and this is usually the case)
        maxTotalBeams = max(totalBeamsArray)

        arrayLength = max(
            max(
                [
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[rayIndex]
                        .position.r
                    )
                    for rayIndex in range(maxTotalBeams)
                ]
                for beamIndex in range(totalWaves)
            )
        )
        len_ray = np.array(
            [[0.0 for _ in range(maxTotalBeams)] for _ in range(totalWaves)]
        ).astype(int)
        x_ray = np.array(
            [
                [[0.0 for _ in range(arrayLength)] for _ in range(maxTotalBeams)]
                for _ in range(totalWaves)
            ]
        )
        y_ray, z_ray, r_ray, phi_ray = (
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
        )

        central_ray_power = np.array(
            [[0.0 for _ in range(arrayLength)] for _ in range(totalWaves)]
        )
        central_ray_powerpar, central_ray_powerperp, central_ray_length = (
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
        )
        wr = []
        for beamIndex in range(totalWaves):
            if activeBeamsArray[beamIndex] == 1:
                for iray in range(maxTotalBeams):
                    if (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[iray]
                        .power_initial
                        != 0
                    ):
                        wr = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.r
                        )
                        wphi = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.phi
                        )
                        wz = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.z
                        )
                        len_ray[beamIndex, iray] = len(wr)
                        r_ray[beamIndex, iray, : len(wr)] = np.array(wr)
                        phi_ray[beamIndex, iray, : len(wphi)] = np.array(wphi)
                        z_ray[beamIndex, iray, : len(wz)] = np.array(wz)
                        x_ray[beamIndex, iray, :] = r_ray[beamIndex, iray, :] * np.cos(
                            phi_ray[beamIndex, iray, :]
                        )
                        y_ray[beamIndex, iray, :] = r_ray[beamIndex, iray, :] * np.sin(
                            phi_ray[beamIndex, iray, :]
                        )
                    npath = len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                    > 0
                ):
                    central_ray_power[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                    > 0
                ):
                    central_ray_powerpar[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                    > 0
                ):
                    central_ray_powerperp[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .length
                    )
                    > 0
                ):
                    central_ray_length[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .length
                    )

        beam_tracing = {"nbeam": totalWaves}
        beam_tracing["nbeam_active"] = len(activeBeamsArray)
        beam_tracing["nray"] = maxTotalBeams
        beam_tracing["is_active"] = activeBeamsArray
        beam_tracing["len_ray"] = len_ray
        beam_tracing["x_ray"] = x_ray
        beam_tracing["y_ray"] = y_ray
        beam_tracing["z_ray"] = z_ray
        beam_tracing["r_ray"] = r_ray
        beam_tracing["phi_ray"] = phi_ray[:, :, : len(wr)]
        beam_tracing["central_ray_power"] = central_ray_power
        beam_tracing["central_ray_powerpar"] = central_ray_powerpar
        beam_tracing["central_ray_powerperp"] = central_ray_powerperp
        beam_tracing["central_ray_length"] = central_ray_length

        return beam_tracing
