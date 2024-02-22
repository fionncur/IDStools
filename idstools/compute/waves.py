""" 
This module provides compute functions and classes for waves ids data

`more about waves ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/waves.html>`_.

"""

import functools
import numpy as np
import logging

logger = logging.getLogger("module")


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
    def getBeams(self, beamTracingTimeIndex: int = 0):
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
        beams = {}

        for beamIndex in range(len(self.ids.coherent_wave)):
            beamDict = {
                "total_beams": len(
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam
                ),
            }
            # Check if any beam has power
            beamDict["active"] = False
            for rayIndex in range(beamDict["total_beams"]):
                if (
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam[rayIndex]
                    .power_initial
                    > 0
                ):
                    beamDict["active"] = True
            beams[beamIndex] = beamDict

        return beams

    def getBeamTracing(self, beamTracingTimeIndex: int = 0):
        """
        This function returns a dictionary containing information about the beam tracing of a coherent wave.

        Args:
            beamTracingTimeIndex (int): The index of the time step for which to retrieve the beam tracing data. Defaults to 0

        Returns:
            a dictionary named "beam_tracing" which contains various arrays and values related to the beam tracing data. Following are the values returned by the function

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134174,117,'public')
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBeamTracing())

        """
        # Count number of active beams and their number of rays
        beamsDict = self.getBeams(beamTracingTimeIndex)

        totalWaves = len(beamsDict.keys())
        beamActivaStatusList = [data["active"] for _, data in beamsDict.items()]
        totalBeamsInEachWaveList = [
            data["total_beams"] for _, data in beamsDict.items()
        ]
        activeBeamsCount = len(
            [data["active"] for _, data in beamsDict.items() if data["active"] is True]
        )

        # We assume the same number of rays for each beam, to simplify (and this is usually the case)
        maxTotalBeams = max(totalBeamsInEachWaveList)

        beamDataLength = max(
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
        beamDataLengthForEachWave = np.array(
            [[0 for _ in range(maxTotalBeams)] for _ in range(totalWaves)]
        )
        beamElectronsLengthForEachWave = np.array(
            [[0 for _ in range(maxTotalBeams)] for _ in range(totalWaves)]
        )
        x_ray = np.array(
            [
                [[0.0 for _ in range(beamDataLength)] for _ in range(maxTotalBeams)]
                for _ in range(totalWaves)
            ]
        )
        y_ray, z_ray, r_ray, phi_ray = (
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
        )

        (
            electronspower,
            powerparallel,
            powerperpendicular,
            length,
        ) = (
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
        )
        for beamIndex in range(totalWaves):
            # To reduce looping
            if beamActivaStatusList[beamIndex] is True:
                for iray in range(maxTotalBeams):
                    ray = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[iray]
                    )
                    if ray.power_initial != 0:  # check individual beam for power check
                        wr = ray.position.r
                        wphi = ray.position.phi
                        wz = ray.position.z

                        beamDataLengthForEachWave[beamIndex, iray] = len(wr)

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
                            .beam[iray]
                            .electrons.power
                        )
                        beamElectronsLengthForEachWave[beamIndex, iray] = npath
                        if len(ray.electrons.power) > 0:
                            electronspower[
                                beamIndex, iray, :npath
                            ] = ray.electrons.power
                        if len(ray.power_flow_norm.parallel) > 0:
                            powerparallel[
                                beamIndex, iray, :npath
                            ] = ray.power_flow_norm.parallel
                        if len(ray.power_flow_norm.perpendicular) > 0:
                            powerperpendicular[
                                beamIndex, iray, :npath
                            ] = ray.power_flow_norm.perpendicular
                        if len(ray.length) > 0:
                            length[beamIndex, iray, :npath] = ray.length

        beam_tracing = {"nbeam": totalWaves}
        beam_tracing["maxTotalBeams"] = maxTotalBeams
        beam_tracing["activeBeamsCount"] = activeBeamsCount
        beam_tracing["beamActivaStatusList"] = beamActivaStatusList
        beam_tracing["beamDataLengthForEachWave"] = beamDataLengthForEachWave
        beam_tracing["beamElectronsLengthForEachWave"] = beamElectronsLengthForEachWave
        beam_tracing["x_ray"] = x_ray
        beam_tracing["y_ray"] = y_ray
        beam_tracing["z_ray"] = z_ray
        beam_tracing["r_ray"] = r_ray
        beam_tracing["phi_ray"] = phi_ray
        beam_tracing["electronspower"] = electronspower
        beam_tracing["powerparallel"] = powerparallel
        beam_tracing["powerperpendicular"] = powerperpendicular
        beam_tracing["length"] = length

        return beam_tracing

    def GetECLaunchersInfo(
        self,
        timeIndex: int = 0,
    ):
        ecLauncherInfo = {}
        data = self.getRadialGridInfo(timeIndex)
        activeLaunchers = {
            key: value for key, value in data.items() if value["isActive"] is True
        }
        _, firstItemValue = next(iter(activeLaunchers.items()))
        nrho = firstItemValue["nrho"]

        timeArray = self.ids.time
        ntime = len(timeArray)
        # LOOP OVER ALL EC LAUNCHERS
        single_ec_launcher_name = dict()
        single_injected_power = dict()  # for the chosen time slice
        single_absorbed_power = dict()  # for the chosen time slice
        single_eccd = dict()  # for the chosen time slice
        total_injected_power = 0  # for the chosen time slice

        total_power_density_profile = [0] * nrho  # profile
        total_current_density_profile = [0] * nrho  # profile
        single_power_density_profile = dict()  # profile
        single_current_density_profile = dict()  # profile

        total_power_waveform = [0] * ntime  # waveform
        total_current_waveform = [0] * ntime  # waveform
        single_power_waveform = dict()  # waveform
        single_current_waveform = dict()  # waveform

        for iwave in range(len(self.ids.coherent_wave)):
            if len(self.ids.coherent_wave[iwave].identifier.antenna_name) > 0:
                single_ec_launcher_name[iwave] = self.ids.coherent_wave[
                    iwave
                ].identifier.antenna_name
            else:
                single_ec_launcher_name[iwave] = f"Launcher{iwave+1}"
            if np.size(self.ids.coherent_wave[iwave].global_quantities) > 0:
                if self.ids.coherent_wave[iwave].global_quantities[0].power > 0:
                    single_power_waveform[iwave] = []
                    single_current_waveform[iwave] = []
                    for itime in range(len(timeArray)):
                        single_power_waveform[iwave].append(
                            self.ids.coherent_wave[iwave]
                            .global_quantities[itime]
                            .electrons.power_thermal
                        )
                        single_current_waveform[iwave].append(
                            self.ids.coherent_wave[iwave]
                            .global_quantities[itime]
                            .current_tor
                        )
                        total_power_waveform[itime] = (
                            total_power_waveform[itime]
                            + self.ids.coherent_wave[iwave]
                            .global_quantities[itime]
                            .electrons.power_thermal
                        )
                        total_current_waveform[itime] = (
                            total_current_waveform[itime]
                            + self.ids.coherent_wave[iwave]
                            .global_quantities[itime]
                            .current_tor
                        )
                    total_power_density_profile = (
                        total_power_density_profile
                        + self.ids.coherent_wave[iwave]
                        .profiles_1d[timeIndex]
                        .power_density
                    )
                    single_power_density_profile[iwave] = (
                        self.ids.coherent_wave[iwave]
                        .profiles_1d[timeIndex]
                        .power_density
                    )
                    total_current_density_profile = (
                        total_current_density_profile
                        + self.ids.coherent_wave[iwave]
                        .profiles_1d[timeIndex]
                        .current_parallel_density
                    )
                    single_current_density_profile[iwave] = (
                        self.ids.coherent_wave[iwave]
                        .profiles_1d[timeIndex]
                        .current_parallel_density
                    )
                    single_injected_power[iwave] = 0.0
                    for ibeam in range(
                        len(self.ids.coherent_wave[iwave].beam_tracing[timeIndex].beam)
                    ):
                        if (
                            self.ids.coherent_wave[iwave]
                            .beam_tracing[timeIndex]
                            .beam[ibeam]
                            .power_initial
                            > 0
                        ):
                            total_injected_power = (
                                total_injected_power
                                + self.ids.coherent_wave[iwave]
                                .beam_tracing[timeIndex]
                                .beam[ibeam]
                                .power_initial
                            )
                            single_injected_power[iwave] = (
                                single_injected_power[iwave]
                                + self.ids.coherent_wave[iwave]
                                .beam_tracing[timeIndex]
                                .beam[ibeam]
                                .power_initial
                            )
                    single_absorbed_power[iwave] = (
                        self.ids.coherent_wave[iwave].global_quantities[timeIndex].power
                    )
                    single_eccd[iwave] = (
                        self.ids.coherent_wave[iwave]
                        .global_quantities[timeIndex]
                        .current_tor
                    )

        ecLauncherInfo["single_ec_launcher_name"] = single_ec_launcher_name
        ecLauncherInfo[
            "single_injected_power"
        ] = single_injected_power  # for the chosen time slice
        ecLauncherInfo[
            "single_absorbed_power"
        ] = single_absorbed_power  # for the chosen time slice
        ecLauncherInfo["single_eccd"] = single_eccd  # for the chosen time slice
        ecLauncherInfo[
            "total_injected_power"
        ] = total_injected_power  # for the chosen time slice

        ecLauncherInfo[
            "total_power_density_profile"
        ] = total_power_density_profile  # profile
        ecLauncherInfo[
            "total_current_density_profile"
        ] = total_current_density_profile  # profile
        ecLauncherInfo[
            "single_power_density_profile"
        ] = single_power_density_profile  # profile
        ecLauncherInfo[
            "single_current_density_profile"
        ] = single_current_density_profile  # profile

        ecLauncherInfo["total_power_waveform"] = total_power_waveform  # waveform
        ecLauncherInfo["total_current_waveform"] = total_current_waveform  # waveform
        ecLauncherInfo["single_power_waveform"] = single_power_waveform  # waveform
        ecLauncherInfo["single_current_waveform"] = single_current_waveform
        return ecLauncherInfo

    def getRadialGridInfo(self, timeIndex: int = 0, usepsi=False):
        """
        The function `getRadialGridInfo` retrieves radial grid information for coherent waves, with an option to use psi as a radial coordinate.

        Args:
            timeIndex (int): The `timeIndex` parameter
            usepsi: The `usepsi` parameter tells whether to use the psi radial coordinate for the grid information.

        Returns:
            The function `getRadialGridInfo` returns a dictionary `data` containing information about the radial grid for each coherent wave in the object. If no active waves are found, it returns `None`.
        """
        data = {}
        activeFound = False
        for iwave in range(len(self.ids.coherent_wave)):
            waveData = {}
            waveData["isActive"] = False
            waveData["isPsiAvailable"] = False
            waveData["npsi"] = None
            waveData["nrho"] = None
            waveData["psi1d"] = None
            waveData["psiBased"] = False
            waveData["rho_tor_norm"] = None

            if np.size(self.ids.coherent_wave[iwave].global_quantities) > 0:
                if self.ids.coherent_wave[iwave].global_quantities[0].power > 0:
                    waveData["isActive"] = True
                    activeFound = True
                    try:
                        if (
                            len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor_norm
                            )
                            > 0
                        ):
                            waveData["nrho"] = len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor_norm
                            )
                            waveData["rho_tor_norm"] = (
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor_norm
                            )
                        elif (
                            len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor
                            )
                            > 0
                        ):
                            waveData["nrho"] = len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor
                            )
                            waveData["rho_tor_norm"] = (
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor
                                / self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.rho_tor[nrho - 1]
                            )
                        elif (
                            len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.psi
                            )
                            > 0
                        ):
                            waveData["psiBased"] = True
                            waveData["nrho"] = len(
                                self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.psi
                            )
                            waveData["rho_tor_norm"] = (
                                -self.ids.coherent_wave[iwave]
                                .profiles_1d[timeIndex]
                                .grid.psi
                            )
                    except:
                        logger.error(
                            "waves.coherent_wave[iwave].profiles_1d[it].grid.rho_tor_norm, rho_tor and psi could not be read"
                        )
                        return None
                    if waveData["nrho"] == 0:
                        logger.error(
                            "waves.coherent_wave[iwave].profiles_1d[it].grid.rho_tor_norm, rho_tor and psi are empty"
                        )
                        return None
                    if (
                        len(
                            self.ids.coherent_wave[iwave]
                            .profiles_1d[timeIndex]
                            .grid.psi
                        )
                        > 0
                    ):
                        waveData["isPsiAvailable"] = True
                        waveData["npsi"] = len(
                            self.ids.coherent_wave[iwave]
                            .profiles_1d[timeIndex]
                            .grid.psi
                        )
                        waveData["psi1d"] = (
                            -self.ids.coherent_wave[iwave]
                            .profiles_1d[timeIndex]
                            .grid.psi
                        )
            else:
                logger.error(
                    "waves.coherent_wave[iwave].global_quantities has not been allocated"
                )
                return None

            if usepsi is True:
                if waveData["isPsiAvailable"] is False:
                    logger.error(
                        "The psi radial coordinate forced but the 1D psi profile is not filled"
                    )
                    return None
                else:
                    waveData["nrho"] = waveData["npsi"]
                    waveData["rho_tor_norm"] = waveData["psi1d"]
                    waveData["psiBased"] = True
            data[iwave] = waveData

        if not activeFound:
            return None
        return data
