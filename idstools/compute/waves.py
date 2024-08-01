"""
This module provides compute functions and classes for waves ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import functools
import numpy as np
import logging
import imas

logger = logging.getLogger("module")


class WavesCompute:
    """This class provides compute functions for waves ids"""

    def __init__(self, ids):
        """Initialization WavesCompute object.

        Args:
            ids : waves ids object
        """
        self.ids = ids

    def get_b_resonance(
        self,
        coherent_wave_index: int = 0,
        time_index: int = 0,
        harmonic_frequencies: list = None,
    ):
        """
        This function calculates the B-resonance (magnetic field) for a given coherent wave index,
        time index, and list of harmonic frequencies.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which we want to calculate the
            B resonance. Defaults to 0
            timeIndex (int): The index of the time step for which the bResonance is being calculated.
            Defaults to 0
            harmonicFrequencies (list): A list of integers representing the harmonic frequencies for
            which the B-resonance values are to be calculated. If this parameter is not provided, the
            function uses the default values of [1, 2, 3, 4].

        Returns:
            A list of values for the magnetic field resonance frequencies for the given coherent wave
            index, time index, and harmonic frequencies. The length of the list is equal to the length of
            the input harmonic frequencies list.


        Notes:
            .. math:: BResonance = \\ 2*pi*ecfrequency*9.1e^-31/1.6e^-19/HarmonicFrequency

            Here harmonicFrequency is any value from [1,2,3,4]

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBResonance())

                [6.0750547938792625, 3.0375273969396313, 2.025018264626421, 1.5187636984698156]
        """
        if harmonic_frequencies is None:
            harmonic_frequencies = [1, 2, 3, 4]
        ec_frequency = self.ids.coherent_wave[coherent_wave_index].global_quantities[time_index].frequency
        b_resonance = [0] * len(harmonic_frequencies)
        for harmonic_frequency_index in range(len(harmonic_frequencies)):
            b_resonance[harmonic_frequency_index] = (
                2 * np.pi * ec_frequency * 9.1e-31 / 1.6e-19 / harmonic_frequencies[harmonic_frequency_index]
            )
        return b_resonance

    def get_beam_array(self):
        """
        This function returns an array of beam indices based on the number of coherent waves.

        Returns:
            a numpy array of equally spaced values from 0 to nbeam-1, where nbeam is the length of the list
            `waves.coherent_wave`. This array represents the indices of the beams.

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBeamArray())

                [ 0.  1.  2.  3.  4.  5.  6.  7.  8.  9. 10.]
        """
        n_beam = len(self.ids.coherent_wave)
        return np.linspace(0, n_beam - 1, n_beam)

    def get_omega_ec(self, coherent_wave_index: int = 0, time_index: int = 0) -> float:
        """
        This function returns the angular frequency of a coherent wave at a specific time index.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which the angular frequency needs to
            be calculated. Defaults to 0
            timeIndex (int): The time index parameter is used to specify the time step for which the frequency
            of the coherent wave is to be retrieved. Defaults to 0

        Returns:
            The value of the angular frequency (in radians per second) of a coherent wave at a specific time
            index. The value is calculated using the frequency of the coherent wave at the given time index
            and multiplying it by 2*pi.

        Notes:
            .. math:: OmegaEC = \\ 2*pi*frequency

        Example:
            .. code-block:: python


                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getOmegaEC())

                1068141502220.5297
        """
        return 2 * np.pi * self.ids.coherent_wave[coherent_wave_index].global_quantities[time_index].frequency

    @functools.lru_cache(maxsize=128)
    def get_beams(self, beam_tracing_time_index: int = 0):
        """
        This function returns a dictionary of active beams with their respective properties.

        Args:
            beamTracingTimeIndex (int): The parameter `beamTracingTimeIndex` is an integer that represents
            the index of the beam tracing time. Defaults to 0

        Returns:
            Dictionary called `activeBeams` which contains information about each beam in `waves.coherent_wave`.
            The dictionary has keys for each beam index and the values are  dictionaries containing the total number
            of beams and boolean indicating whether the beam is active or not. The function determines if a beam
            is active by checking if any of its rays have initial power greater than 0.

        Example:
            .. code-block:: python


                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
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

        for beam_index in range(len(self.ids.coherent_wave)):
            beam_dict = {
                "total_beams": len(self.ids.coherent_wave[beam_index].beam_tracing[beam_tracing_time_index].beam),
            }
            # Check if any beam has power
            beam_dict["active"] = False
            for ray_index in range(beam_dict["total_beams"]):
                if (
                    self.ids.coherent_wave[beam_index]
                    .beam_tracing[beam_tracing_time_index]
                    .beam[ray_index]
                    .power_initial
                    > 0
                ):
                    beam_dict["active"] = True
            beams[beam_index] = beam_dict

        return beams

    def get_beam_tracing(self, beam_tracing_time_index: int = 0):
        """
        This function returns a dictionary containing information about the beam tracing of a coherent wave.

        Args:
            beamTracingTimeIndex (int): The index of the time step for which to retrieve the beam tracing data.
            Defaults to 0

        Returns:
            a dictionary named "beam_tracing" which contains various arrays and values related to the beam tracing
            data. Following are the values returned by the function

        Example:
            .. code-block:: python

                import imas
                from idstools.compute.waves import WavesCompute

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
                connection.open()
                idsObj = connection.get('waves')
                waveobj = WavesCompute(waves_ids)
                print(waveobj.getBeamTracing())

        """
        # Count number of active beams and their number of rays
        beams_dict = self.get_beams(beam_tracing_time_index)

        total_waves = len(beams_dict.keys())
        beam_activa_status_list = [data["active"] for _, data in beams_dict.items()]
        total_beams_in_each_wave_list = [data["total_beams"] for _, data in beams_dict.items()]
        active_beams_count = len([data["active"] for _, data in beams_dict.items() if data["active"] is True])

        # We assume the same number of rays for each beam, to simplify (and this is usually the case)
        max_total_beams = max(total_beams_in_each_wave_list)

        beam_data_length = max(
            max(
                [
                    len(
                        self.ids.coherent_wave[beam_index]
                        .beam_tracing[beam_tracing_time_index]
                        .beam[ray_index]
                        .position.r
                    )
                    for ray_index in range(max_total_beams)
                ]
                for beam_index in range(total_waves)
            )
        )
        beam_data_length_for_each_wave = np.array([[0 for _ in range(max_total_beams)] for _ in range(total_waves)])
        beam_electrons_length_for_each_wave = np.array(
            [[0 for _ in range(max_total_beams)] for _ in range(total_waves)]
        )
        len_ray = np.array([[0.0 for iray in range(max_total_beams)] for ibeam in range(total_waves)]).astype(int)
        x_ray = np.array(
            [[[0.0 for _ in range(beam_data_length)] for _ in range(max_total_beams)] for _ in range(total_waves)]
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
        for beam_index in range(total_waves):
            # To reduce looping
            if beam_activa_status_list[beam_index] is True:
                for iray in range(max_total_beams):
                    ray = self.ids.coherent_wave[beam_index].beam_tracing[beam_tracing_time_index].beam[iray]
                    if ray.power_initial != 0:  # check individual beam for power check
                        wr = ray.position.r
                        wphi = ray.position.phi
                        wz = ray.position.z

                        beam_data_length_for_each_wave[beam_index, iray] = len(wr)

                        r_ray[beam_index, iray, : len(wr)] = np.array(wr)
                        phi_ray[beam_index, iray, : len(wphi)] = np.array(wphi)
                        z_ray[beam_index, iray, : len(wz)] = np.array(wz)

                        x_ray[beam_index, iray, :] = r_ray[beam_index, iray, :] * np.cos(phi_ray[beam_index, iray, :])
                        y_ray[beam_index, iray, :] = r_ray[beam_index, iray, :] * np.sin(phi_ray[beam_index, iray, :])
                        len_ray[beam_index, iray] = len(wr)
                        npath = len(
                            self.ids.coherent_wave[beam_index]
                            .beam_tracing[beam_tracing_time_index]
                            .beam[iray]
                            .electrons.power
                        )
                        beam_electrons_length_for_each_wave[beam_index, iray] = npath
                        if len(ray.electrons.power) > 0:
                            electronspower[beam_index, iray, :npath] = ray.electrons.power
                        if len(ray.power_flow_norm.parallel) > 0:
                            powerparallel[beam_index, iray, :npath] = ray.power_flow_norm.parallel
                        if len(ray.power_flow_norm.perpendicular) > 0:
                            powerperpendicular[beam_index, iray, :npath] = ray.power_flow_norm.perpendicular
                        if len(ray.length) > 0:
                            length[beam_index, iray, :npath] = ray.length

        beam_tracing = {"nbeam": total_waves}
        beam_tracing["maxTotalBeams"] = max_total_beams
        beam_tracing["activeBeamsCount"] = active_beams_count
        beam_tracing["beamActivaStatusList"] = beam_activa_status_list
        beam_tracing["beamDataLengthForEachWave"] = beam_data_length_for_each_wave
        beam_tracing["beamElectronsLengthForEachWave"] = beam_electrons_length_for_each_wave
        beam_tracing["x_ray"] = x_ray
        beam_tracing["len_ray"] = len_ray
        beam_tracing["y_ray"] = y_ray
        beam_tracing["z_ray"] = z_ray
        beam_tracing["r_ray"] = r_ray
        beam_tracing["phi_ray"] = phi_ray
        beam_tracing["electronspower"] = electronspower
        beam_tracing["powerparallel"] = powerparallel
        beam_tracing["powerperpendicular"] = powerperpendicular
        beam_tracing["length"] = length

        return beam_tracing

    def get_e_c_launchers_info(self, time_index: int = 0, usepsi=False, verbose=False):
        ec_launcher_info = {}
        data = self.get_radial_grid_info(time_index, usepsi)
        active_launchers = {key: value for key, value in data.items() if value["isActive"] is True}
        _, first_item_value = next(iter(active_launchers.items()))
        nrho = first_item_value["nrho"]

        time_array = self.ids.time
        ntime = len(time_array)
        # LOOP OVER ALL EC LAUNCHERS
        single_ec_launcher_name = dict()
        single_injected_power = dict()  # for the chosen time slice
        single_absorbed_power = dict()  # for the chosen time slice
        single_eccd = dict()  # for the chosen time slice
        total_injected_power = 0  # for the chosen time slice

        total_absorbed_power = 0
        total_eccd = 0
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
                single_ec_launcher_name[iwave] = self.ids.coherent_wave[iwave].identifier.antenna_name
            else:
                single_ec_launcher_name[iwave] = f"Launcher{iwave+1}"
            if np.size(self.ids.coherent_wave[iwave].global_quantities) > 0:
                if self.is_active_during_pulse(iwave) is True:
                    single_power_waveform[iwave] = []
                    single_current_waveform[iwave] = []
                    for itime in range(len(time_array)):
                        single_power_waveform[iwave].append(
                            self.ids.coherent_wave[iwave].global_quantities[itime].electrons.power_thermal
                        )
                        single_current_waveform[iwave].append(
                            self.ids.coherent_wave[iwave].global_quantities[itime].current_tor
                        )
                        total_power_waveform[itime] = (
                            total_power_waveform[itime]
                            + self.ids.coherent_wave[iwave].global_quantities[itime].electrons.power_thermal
                        )
                        total_current_waveform[itime] = (
                            total_current_waveform[itime]
                            + self.ids.coherent_wave[iwave].global_quantities[itime].current_tor
                        )
                    if len(self.ids.coherent_wave[iwave].profiles_1d[time_index].power_density) > 0:
                        total_power_density_profile = (
                            total_power_density_profile
                            + self.ids.coherent_wave[iwave].profiles_1d[time_index].power_density
                        )
                    if len(self.ids.coherent_wave[iwave].profiles_1d[time_index].power_density) > 0:
                        single_power_density_profile[iwave] = (
                            self.ids.coherent_wave[iwave].profiles_1d[time_index].power_density
                        )
                    if len(self.ids.coherent_wave[iwave].profiles_1d[time_index].current_parallel_density) > 0:
                        total_current_density_profile = (
                            total_current_density_profile
                            + self.ids.coherent_wave[iwave].profiles_1d[time_index].current_parallel_density
                        )
                        single_current_density_profile[iwave] = (
                            self.ids.coherent_wave[iwave].profiles_1d[time_index].current_parallel_density
                        )
                    single_injected_power[iwave] = 0.0
                    if len(self.ids.coherent_wave[iwave].beam_tracing) > 0:
                        for ibeam in range(len(self.ids.coherent_wave[iwave].beam_tracing[time_index].beam)):
                            if imas.imasdef.isFieldValid(
                                self.ids.coherent_wave[iwave].beam_tracing[time_index].beam[ibeam].power_initial
                            ) and (
                                self.ids.coherent_wave[iwave].beam_tracing[time_index].beam[ibeam].power_initial > 0
                            ):
                                total_injected_power = (
                                    total_injected_power
                                    + self.ids.coherent_wave[iwave].beam_tracing[time_index].beam[ibeam].power_initial
                                )
                                single_injected_power[iwave] = (
                                    single_injected_power[iwave]
                                    + self.ids.coherent_wave[iwave].beam_tracing[time_index].beam[ibeam].power_initial
                                )

                                total_absorbed_power = (
                                    total_absorbed_power
                                    + self.ids.coherent_wave[iwave].global_quantities[time_index].power
                                )
                                total_eccd = (
                                    total_eccd + self.ids.coherent_wave[iwave].global_quantities[time_index].current_tor
                                )

                    single_absorbed_power[iwave] = self.ids.coherent_wave[iwave].global_quantities[time_index].power
                    single_eccd[iwave] = self.ids.coherent_wave[iwave].global_quantities[time_index].current_tor
                    if verbose:
                        logger.info(
                            " "
                            + single_ec_launcher_name[iwave]
                            + " is active with a power of {:.2f}".format(single_injected_power[iwave] * 1.0e-6)
                            + " MW"
                        )
                        logger.info(
                            "   --> Absorbed power = {:.2f}".format(single_absorbed_power[iwave] * 1.0e-6) + " MW"
                        )
                        logger.info("   --> Curent Drive =  {:.2e}".format(single_eccd[iwave] * 1.0e-3) + " kA")
                        logger.info("Total injected power = {:.2f}".format(total_injected_power * 1.0e-6) + " MW")
                        logger.info("Total absorbed power = {:.2f}".format(total_absorbed_power * 1.0e-6) + " MW")
                        logger.info("Total ECCD           = {:.2f}".format(total_eccd * 1.0e-6) + " MA")
                else:
                    if verbose:
                        logger.info(" " + single_ec_launcher_name[iwave] + " is off")

        ec_launcher_info["single_ec_launcher_name"] = single_ec_launcher_name
        ec_launcher_info["single_injected_power"] = single_injected_power  # for the chosen time slice
        ec_launcher_info["single_absorbed_power"] = single_absorbed_power  # for the chosen time slice
        ec_launcher_info["single_eccd"] = single_eccd  # for the chosen time slice
        ec_launcher_info["total_injected_power"] = total_injected_power  # for the chosen time slice

        ec_launcher_info["total_absorbed_power"] = total_absorbed_power  # for the chosen time slice
        ec_launcher_info["total_eccd"] = total_eccd

        ec_launcher_info["total_power_density_profile"] = total_power_density_profile  # profile
        ec_launcher_info["total_current_density_profile"] = total_current_density_profile  # profile
        ec_launcher_info["single_power_density_profile"] = single_power_density_profile  # profile
        ec_launcher_info["single_current_density_profile"] = single_current_density_profile  # profile

        ec_launcher_info["total_power_waveform"] = total_power_waveform  # waveform
        ec_launcher_info["total_current_waveform"] = total_current_waveform  # waveform
        ec_launcher_info["single_power_waveform"] = single_power_waveform  # waveform
        ec_launcher_info["single_current_waveform"] = single_current_waveform
        return ec_launcher_info

    def get_radial_grid_info(self, time_index: int = 0, usepsi=False):
        """
        The function `getRadialGridInfo` retrieves radial grid information for coherent waves, with an option
        to use psi as a radial coordinate.

        Args:
            timeIndex (int): The `timeIndex` parameter
            usepsi: The `usepsi` parameter tells whether to use the psi radial coordinate for the grid information.

        Returns:
            The function `getRadialGridInfo` returns a dictionary `data` containing information about the
            radial grid for each coherent wave in the object. If no active waves are found, it returns `None`.
        """
        data = {}
        active_found = False
        for iwave in range(len(self.ids.coherent_wave)):
            wave_data = {}
            wave_data["isActive"] = False
            wave_data["isPsiAvailable"] = False
            wave_data["npsi"] = None
            wave_data["nrho"] = None
            wave_data["psi1d"] = None
            wave_data["psiBased"] = False
            wave_data["rho_tor_norm"] = None

            if np.size(self.ids.coherent_wave[iwave].global_quantities) > 0:
                if self.is_active_during_pulse(iwave) is True:
                    wave_data["isActive"] = True
                    active_found = True
                    try:
                        if len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor_norm) > 0:
                            wave_data["nrho"] = len(
                                self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor_norm
                            )
                            wave_data["rho_tor_norm"] = (
                                self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor_norm
                            )
                        elif len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor) > 0:
                            wave_data["nrho"] = len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor)
                            wave_data["rho_tor_norm"] = (
                                self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.rho_tor
                                / self.ids.coherent_wave[iwave]
                                .profiles_1d[time_index]
                                .grid.rho_tor[wave_data["nrho"] - 1]
                            )
                        elif len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi) > 0:
                            wave_data["psiBased"] = True
                            wave_data["nrho"] = len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi)
                            wave_data["rho_tor_norm"] = -self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi
                    except Exception as e:
                        logger.debug(f"{e}")
                        logger.error(
                            "waves.coherent_wave[iwave].profiles_1d[it].grid.rho_tor_norm, \
                            rho_tor and psi could not be read"
                        )
                        return None
                    if wave_data["nrho"] == 0:
                        logger.error(
                            "waves.coherent_wave[iwave].profiles_1d[it].grid.rho_tor_norm, \
                            rho_tor and psi are empty"
                        )
                        return None
                    if len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi) > 0:
                        wave_data["isPsiAvailable"] = True
                        wave_data["npsi"] = len(self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi)
                        wave_data["psi1d"] = -self.ids.coherent_wave[iwave].profiles_1d[time_index].grid.psi
            else:
                logger.error("waves.coherent_wave[iwave].global_quantities has not been allocated")
                return None

            if usepsi is True:
                if wave_data["isPsiAvailable"] is False:
                    logger.error("The psi radial coordinate forced but the 1D psi profile is not filled")
                    return None
                else:
                    wave_data["nrho"] = wave_data["npsi"]
                    wave_data["rho_tor_norm"] = wave_data["psi1d"]
                    wave_data["psiBased"] = True
            data[iwave] = wave_data

        if not active_found:
            return None
        return data

    def is_active_during_pulse(self, wave_index):
        for itime in range(len(self.ids.time)):
            if self.ids.coherent_wave[wave_index].global_quantities[itime].power > 0:
                return True
        return False
