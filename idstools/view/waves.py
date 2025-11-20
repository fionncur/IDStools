import logging

import numpy as np

from idstools.compute.common import find_maxima, find_minima, findfwhm
from idstools.compute.waves import WavesCompute

logger = logging.getLogger(f"module.{__name__}")


class WavesView:
    def __init__(self, ids):
        self.waves_compute = WavesCompute(ids)
        self.ids = ids

    def plot_pol_view_traces(self, ax, time_slice, color="b", style="-", label=""):
        beam_tracing_dict = self.waves_compute.get_beam_tracing(time_slice)
        beam_data_length_for_each_wave = beam_tracing_dict["beam_data_length_for_each_wave"]

        length_data = beam_tracing_dict["length"]
        r_ray_data = beam_tracing_dict["r_ray"]
        z_ray_data = beam_tracing_dict["z_ray"]
        display_label_once = True
        for i in range(len(length_data)):
            for j in range(len(length_data[i])):
                length = beam_data_length_for_each_wave[i][j]
                r_ray = r_ray_data[i][j]
                z_ray = z_ray_data[i][j]
                ax.plot(
                    r_ray[:length],
                    z_ray[:length],
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if display_label_once is True:
                    display_label_once = False
                    label = ""

    def plot_top_view_traces(self, ax, time_slice, color="b", style="-", label=""):
        ax.set_title("Top View (X,Y)")
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")

        beam_tracing_dict = self.waves_compute.get_beam_tracing(time_slice)
        beam_data_length_for_each_wave = beam_tracing_dict["beam_data_length_for_each_wave"]
        length_data = beam_tracing_dict["length"]
        x_ray_data = beam_tracing_dict["x_ray"]
        y_ray_data = beam_tracing_dict["y_ray"]
        display_label_once = True
        for i in range(len(length_data)):
            for j in range(len(length_data[i])):
                length = beam_data_length_for_each_wave[i][j]
                x_ray = x_ray_data[i][j]
                y_ray = y_ray_data[i][j]

                ax.plot(
                    x_ray[:length],
                    y_ray[:length],
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if display_label_once is True:
                    display_label_once = False
                    label = ""

    def plot_electron_power(self, ax, time_slice, color="b", style="-", label=""):
        ax.set_title("Power along the beams")
        ax.set_xlabel("Path length [m]")
        ax.set_ylabel("P$_{electrons}$ [MW]")

        beam_tracing_dict = self.waves_compute.get_beam_tracing(time_slice)
        beam_electrons_length_for_each_wave = beam_tracing_dict["beam_electrons_length_for_each_wave"]

        length_data = beam_tracing_dict["length"]
        electronspower_data = beam_tracing_dict["electronspower"]
        display_label_once = True
        label = "Electrons Power [W]"
        for i in range(len(length_data)):
            for j in range(len(length_data[i])):
                dlength = beam_electrons_length_for_each_wave[i][j]
                length = length_data[i][j]
                electronspower = electronspower_data[i][j]

                ax.plot(
                    length[:dlength],
                    electronspower[:dlength] * 1.0e-6,
                    color=color,
                    linestyle=style,
                    label=label,
                )
                if display_label_once is True:
                    display_label_once = False
                    label = ""
        ax.legend()

    def plot_power_flow_normal(self, ax, time_slice, color="b", style="-", label=""):
        ax.set_title("Power flow to the magnetic field")
        ax.set_xlabel("Path length [m]")

        beam_tracing_dict = self.waves_compute.get_beam_tracing(time_slice)
        beam_electrons_length_for_each_wave = beam_tracing_dict["beam_electrons_length_for_each_wave"]

        length_data = beam_tracing_dict["length"]
        powerparallel_data = beam_tracing_dict["powerparallel"]
        powerperpendicular_data = beam_tracing_dict["powerperpendicular"]
        perplabel = "P$_\\perp$/P$_{max}$ [-]"
        parlabel = "P$_\\parallel$/P$_{max}$ [-]"
        display_label_once = True
        for i in range(len(length_data)):
            for j in range(len(length_data[i])):
                dlength = beam_electrons_length_for_each_wave[i][j]
                length = length_data[i][j]
                powerparallel = powerparallel_data[i][j]
                powerperpendicular = powerperpendicular_data[i][j]

                ax.plot(
                    length[:dlength],
                    powerparallel[:dlength],
                    color="b",
                    linestyle=style,
                    label=parlabel,
                )
                ax.plot(
                    length[:dlength],
                    powerperpendicular[:dlength],
                    color="r",
                    linestyle=style,
                    label=perplabel,
                )
                if display_label_once is True:
                    display_label_once = False
                    perplabel = ""
                    parlabel = ""
        ax.legend()

    def plot_ecrh_profiles(
        self,
        ax,
        time_slice,
        verbose=False,
    ):
        # ECRH PROFILE [MA/M2]
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice)
        radial_grid = self.waves_compute.get_radial_grid_info(time_slice)
        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        _, first_radial_grid_info = next(iter(active_launchers.items()))

        code_name = self.ids.code.name.upper()
        ax.set_title("ECRH Profiles")
        len_active_launchers = len(active_launchers)
        if len_active_launchers != 0:
            totalx1 = first_radial_grid_info["rho_tor_norm"]
            totaly1 = ec_launcher_info["total_power_density_profile"] * 1.0e-6
            totallabel1 = f"Total-{code_name}"

            ax.plot(totalx1, totaly1, label=totallabel1)
            if verbose:
                maxima = find_maxima(totaly1)
                logger.info(f"There are {len(maxima) - 1} maxima")
                fwhm = []
                for i in range(len(maxima)):
                    if i == 0:
                        fwhm.append(
                            findfwhm(
                                totalx1,
                                totaly1,
                                maxima[0],
                                0,
                                (maxima[0] + maxima[1]) // 2,
                            )
                        )
                    elif i == len(maxima) - 1:
                        fwhm.append(
                            findfwhm(
                                totalx1,
                                totaly1,
                                maxima[i],
                                (maxima[i - 1] + maxima[i]) // 2,
                                len(totaly1),
                            )
                        )
                        logger.info(f"({totalx1[maxima[i]]}, {totaly1[maxima[i]]} --- fwhm: {fwhm[i]})")
                    else:
                        fwhm.append(
                            findfwhm(
                                totalx1,
                                totaly1,
                                maxima[i],
                                (maxima[i - 1] + maxima[i]) // 2,
                                (maxima[i] + maxima[i + 1]) // 2,
                            )
                        )
                        logger.info(f"({totalx1[maxima[i]]}, {totaly1[maxima[i]]} --- fwhm: {fwhm[i]})")

            for i_wave, _ in active_launchers.items():
                ax.plot(
                    first_radial_grid_info["rho_tor_norm"],
                    ec_launcher_info["single_power_density_profile"][i_wave] * 1.0e-6,
                    linestyle="--",
                    label=ec_launcher_info["single_ec_launcher_name"][i_wave],
                )
            ax.set_ylabel("Absorbed power $\\mathrm{[MW/m^{3}]}$")
            if first_radial_grid_info["psiBased"] is False:
                ax.set_xlabel("Normalized toroidal flux coordinate")
            else:
                ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
            ax.legend()

    def plot_eccd_profiles(
        self,
        ax,
        time_slice,
        verbose=False,
    ):
        # ECCD PROFILE [MA/M2]
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice)
        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        _, first_radial_grid_info = next(iter(active_launchers.items()))

        code_name = self.ids.code.name.upper()
        ax.set_title("ECCD Profiles")

        len_active_launchers = len(active_launchers)
        if len_active_launchers != 0:
            totalx2 = first_radial_grid_info["rho_tor_norm"]
            totaly2 = ec_launcher_info["total_current_density_profile"] * 1.0e-6
            totallabel = f"Total-{code_name}"
            ax.plot(totalx2, totaly2, label=totallabel)
            if verbose:
                minima = find_minima(totaly2)
                logger.info(f"There are {len(minima)} minima")
                fwhm = []
                for i in range(len(minima)):
                    if i == 0:
                        fwhm.append(findfwhm(totalx2, totaly2, minima[0], 0, (minima[0] + minima[1]) // 2))
                    elif i == len(minima) - 1:
                        fwhm.append(
                            findfwhm(totalx2, totaly2, minima[i], (minima[i - 1] + minima[i]) // 2, len(totaly2))
                        )
                    else:
                        fwhm.append(
                            findfwhm(
                                totalx2,
                                totaly2,
                                minima[i],
                                (minima[i - 1] + minima[i]) // 2,
                                (minima[i] + minima[i + 1]) // 2,
                            )
                        )
                    logger.info(f"({totalx2[minima[i]]}, {totaly2[minima[i]]} --- fwhm: {fwhm[i]})")
            # logger.debug(fwhm)
        for i_wave, _ in active_launchers.items():
            ax.plot(
                first_radial_grid_info["rho_tor_norm"],
                ec_launcher_info["single_current_density_profile"][i_wave] * 1.0e-6,
                linestyle="--",
                label=ec_launcher_info["single_ec_launcher_name"][i_wave],
            )
        ax.set_ylabel(r"$\mathrm{ECCD} \ [\text{MA}/\text{m}^{2}]$")
        # ax.set_ylabel(r"$\mathrm{ECCD} \; [\mathrm{MA}/\mathrm{m}^{2}]$")
        if first_radial_grid_info["psiBased"] is False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        ax.legend()

    def plot_ecrh_waveform(
        self,
        ax,
        time_slice,
    ):
        time_array = self.ids.time
        ntime = len(self.ids.time)
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice)
        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}

        code_name = self.ids.code.name.upper()

        ax.set_title("ECRH Waveforms")

        if ntime == 1:
            logger.error("Only one time slice --> ECRH and ECCD waveforms not displayed")
            return -1
        else:
            ax.set_title("ECRH Waveforms")
            ax.set_ylabel("Power to the electrons $\\mathrm{[MW]}$")
            ax.set_xlabel("Time (s)")
            # EC POWER WAVEFORM
            if len(active_launchers) > 0:
                ax.plot(
                    time_array,
                    np.array(ec_launcher_info["total_power_waveform"]) * 1.0e-6,
                    label=f"Total-{code_name}",
                )
            for i_wave, _ in active_launchers.items():
                ax.plot(
                    time_array,
                    np.array(ec_launcher_info["single_power_waveform"][i_wave]) * 1.0e-6,
                    linestyle="--",
                    label=ec_launcher_info["single_ec_launcher_name"][i_wave],
                )
            ax.legend()
            return 0

    def plot_e_c_c_d_waveform(
        self,
        ax,
        time_slice,
    ):
        time_array = self.ids.time
        ntime = len(self.ids.time)
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice)
        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}

        code_name = self.ids.code.name.upper()

        ax.set_title("ECCD Waveforms")

        if ntime == 1:
            logger.error("Only one time slice --> ECCD waveforms not displayed")
            return -1
        else:
            ax.set_title("ECCD Waveforms")
            ax.set_ylabel("ECCD $\\mathrm{[kA]}$")
            ax.set_xlabel("Time (s)")
            # EC POWER WAVEFORM
            if len(active_launchers) > 0:
                ax.plot(
                    time_array,
                    np.array(ec_launcher_info["total_current_waveform"]) * 1.0e-3,
                    label=f"Total-{code_name}",
                )
            for i_wave, _ in active_launchers.items():
                ax.plot(
                    time_array,
                    np.array(ec_launcher_info["single_current_waveform"][i_wave]) * 1.0e-6,
                    linestyle="--",
                    label=ec_launcher_info["single_ec_launcher_name"][i_wave],
                )
            ax.legend()
            return 0

    def display_e_c_launchers_info(self, time_slice):
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice)

        launchers = self.waves_compute.get_radial_grid_info(time_slice)

        for i_wave, wave_data in launchers.items():
            if wave_data["is_active"] is True:
                logger.info(
                    f"{ec_launcher_info['single_ec_launcher_name'][i_wave]} is active with a power of"
                    f"{ec_launcher_info['single_injected_power'][i_wave] * 1.e-6:.2f} MW --> Absorbed power ="
                    f"{ec_launcher_info['single_absorbed_power'][i_wave] * 1.e-6:.2f} MW"
                )
                logger.info(f"--> ECCD =  {ec_launcher_info['single_eccd'][i_wave] * 1.e-3:.2f} kA")
            else:
                logger.info(f"{ec_launcher_info['single_ec_launcher_name'][i_wave]} is off")

    # CD WAVEFORM
    def view_c_d_waveform(self, ax, time_slice, usepsi=False):
        time_array = self.ids.time
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice, usepsi)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice, usepsi)

        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        len_active_launchers = len(active_launchers)
        ax.set_title("Current density waveform")
        if len_active_launchers != 0:
            ax.plot(
                time_array,
                np.array(ec_launcher_info["total_current_waveform"]) * 1.0e-3,
                label=r"Total",
            )
        for iwave, _ in active_launchers.items():
            ax.plot(
                time_array,
                np.array(ec_launcher_info["single_current_waveform"][iwave]) * 1.0e-3,
                label=ec_launcher_info["single_ec_launcher_name"][iwave],
            )
        ax.set_ylabel("Current Density $\\mathrm{[kA]}$")
        ax.set_xlabel("Time (s)")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # EC POWER WAVEFORM
    def view_e_c_power_waveform(self, ax, time_slice, usepsi=False):
        time_array = self.ids.time
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice, usepsi)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice, usepsi)

        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        len_active_launchers = len(active_launchers)
        ax.set_title("EC Power Waveform")
        if len_active_launchers != 0:
            ax.plot(
                time_array,
                np.array(ec_launcher_info["total_power_waveform"]) * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in active_launchers.items():
            ax.plot(
                time_array,
                np.array(ec_launcher_info["single_power_waveform"][iwave]) * 1.0e-6,
                label=ec_launcher_info["single_ec_launcher_name"][iwave],
            )
        ax.set_ylabel("Power to the electrons $\\mathrm{[MW]}$")
        ax.set_xlabel("Time (s)")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # CD PROFILE [MA/M2]
    def view_c_d_profile(self, ax, time_slice, usepsi=False):
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice, usepsi)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice, usepsi)

        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        _, first_radial_grid_info = next(iter(active_launchers.items()))
        len_active_launchers = len(active_launchers)
        ax.set_title("Current density profile")
        if len_active_launchers != 0:
            ax.plot(
                first_radial_grid_info["rho_tor_norm"],
                ec_launcher_info["total_current_density_profile"] * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in active_launchers.items():
            if iwave in ec_launcher_info["single_current_density_profile"]:
                ax.plot(
                    first_radial_grid_info["rho_tor_norm"],
                    ec_launcher_info["single_current_density_profile"][iwave] * 1.0e-6,
                    label=ec_launcher_info["single_ec_launcher_name"][iwave],
                )
        ax.set_ylabel(r"$\mathrm{CD} \ [\text{MA}/\text{m}^{2}]$")
        # ax.set_ylabel("$\\mathrm{CD} [MA/m^{2}]}$")
        if first_radial_grid_info["psiBased"] is False and usepsi is False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # PROFILE OF ABSORBED POWER DENSITY [MW/M3]
    def view_absorbed_power_density_profile(self, ax, time_slice, usepsi=False):
        ec_launcher_info = self.waves_compute.get_ec_launchers_info(time_slice, usepsi, True)

        radial_grid = self.waves_compute.get_radial_grid_info(time_slice, usepsi)

        active_launchers = {key: value for key, value in radial_grid.items() if value["is_active"] is True}
        _, first_radial_grid_info = next(iter(active_launchers.items()))
        len_active_launchers = len(active_launchers)
        ax.set_title("Absorbed power density profile")
        if len_active_launchers != 0:
            ax.plot(
                first_radial_grid_info["rho_tor_norm"],
                ec_launcher_info["total_power_density_profile"] * 1.0e-6,
                label=r"Total",
            )
        for iwave, _ in active_launchers.items():
            if iwave in ec_launcher_info["single_power_density_profile"]:
                ax.plot(
                    first_radial_grid_info["rho_tor_norm"],
                    ec_launcher_info["single_power_density_profile"][iwave] * 1.0e-6,
                    label=ec_launcher_info["single_ec_launcher_name"][iwave],
                )
        ax.set_ylabel("Absorbed power $\\mathrm{[MW/m^{3}]}$")
        if first_radial_grid_info["psiBased"] is False and usepsi is False:
            ax.set_xlabel("Normalized toroidal flux coordinate")
        else:
            ax.set_xlabel("-(Poloidal flux coordinate) [Wb]")
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def plot_beam_index(self, ax):
        """
        This function plots a bar graph of beam indices with a fixed height of 20.

        Args:
            ax: ax is a matplotlib axis object
        """
        # TODO add callback function which can be called whenever there is update requested on timeline
        beam_array = self.waves_compute.get_beam_array()
        ax.bar(beam_array, 20, color="g", width=0.5)
        ax.set_xlim(beam_array[0] - 1, beam_array[-1] + 1)
        ax.set_ylim(top=20)

    def plot_poloidal_traces_update(self, ax, time_slice, verbose=False, update=True):
        # Read beam tracing from waves IDS
        beam_tracing = self.waves_compute.get_beam_tracing(time_slice)

        nbeam = beam_tracing["nbeam"]
        nbeam_active = beam_tracing["active_beams_count"]
        nray = beam_tracing["max_total_beams"]
        is_active = beam_tracing["beam_active_status_list"]
        len_ray = beam_tracing["len_ray"]
        z_ray = beam_tracing["z_ray"]
        r_ray = beam_tracing["r_ray"]

        if verbose:
            if nbeam_active > 1:
                logger.info(
                    "There are "
                    + str(nbeam_active)
                    + " active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                logger.info(
                    "There is "
                    + str(nbeam_active)
                    + " active beam and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )

        ax_polview_plot_traces = {}

        for ibeam in range(nbeam):
            # ax_polview_plot_traces[ibeam] = {}
            if is_active[ibeam] is True:

                for iray in range(nray):
                    # TODO: update mechanism needs to be centralized
                    if update is True:

                        (ax_polview_plot_traces[iray],) = ax.plot(
                            r_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            z_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            color="b",
                            linestyle="-",
                        )
                    else:
                        ax[iray].set_data(
                            r_ray[ibeam, iray, : len_ray[ibeam, iray]],
                            z_ray[ibeam, iray, : len_ray[ibeam, iray]],
                        )
        return ax_polview_plot_traces

    def plot_topview_traces_update(self, ax, time_slice, verbose=False, update=True):
        # Read beam tracing from waves IDS
        beam_tracing = self.waves_compute.get_beam_tracing(time_slice)
        nbeam = beam_tracing["nbeam"]
        is_active = beam_tracing["beam_active_status_list"]
        len_ray = beam_tracing["len_ray"]
        x_ray = beam_tracing["x_ray"]
        y_ray = beam_tracing["y_ray"]

        nray = beam_tracing["max_total_beams"]
        if verbose:
            nbeam_active = beam_tracing["nbeam_active"]
            if nbeam_active > 1:
                print(
                    f"There are {str(nbeam_active)} active beam"
                    + int(nbeam_active != 1) * "s and each beam has "
                    + str(nray)
                    + " ray"
                    + int(nray != 1) * "s"
                )
            else:
                print(
                    f"There is {str(nbeam_active)} active beam and each beam has {str(nray)} ray" + int(nray != 1) * "s"
                )

        ax_topview_plot_traces = {}
        for beam_index in range(nbeam):
            # ax_topview_plot_traces[ibeam] = {}
            if is_active[beam_index] == 1:
                color = "b"
                style = "-"

                for iray in range(nray):
                    if update == 1:
                        (ax_topview_plot_traces[iray],) = ax.plot(
                            x_ray[beam_index, iray, : len_ray[beam_index, iray]],
                            y_ray[beam_index, iray, : len_ray[beam_index, iray]],
                            color=color,
                            linestyle=style,
                        )
                    else:
                        ax[iray].set_data(
                            x_ray[beam_index, iray, : len_ray[beam_index, iray]],
                            y_ray[beam_index, iray, : len_ray[beam_index, iray]],
                        )
        if update == 1:
            return ax_topview_plot_traces
