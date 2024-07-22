import logging

import numpy as np

from idstools.compute.distributions import DistributionsCompute

logger = logging.getLogger(f"module.{__name__}")


class distributions_view:
    def __init__(self, ids):
        self.distributions_compute = distributions_compute(ids)
        self.ids = ids

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plot_absorbed_power_density_individual(
        self,
        ax,
        time_index,
    ):
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_index)
        profiles = self.distributions_compute.get_profiles(time_index)

        if len(self.distributions_compute.active_distributions) != 0:
            ax.plot(
                self.distributions_compute.rho_tor_norm,
                profiles["all_injectors_total_power_density_profile"] * 1.0e-6,
                label=r"All injectors",
                color="black",
            )
            for idistrib in range(self.distributions_compute.ndistributions):
                if radial_grid_info[idistrib]["is_active"]:
                    lbl = ""
                    if idistrib == 0 or self.distributions_compute.ndistributions - 1 == idistrib:
                        lbl = profiles["single_nf_source_name"][idistrib]
                    # ax.plot(self.distributionsCompute.rho_tor_norm,
                    # profiles['single_total_power_density_profile'][idistrib]*1.e-6,
                    # label=profiles['single_nf_source_name'][idistrib])
                    ax.plot(
                        self.distributions_compute.rho_tor_norm,
                        profiles["single_total_power_density_profile"][idistrib] * 1.0e-6,
                        label=lbl,
                    )
        ax.set_title("NBI/FUS power individual injectors profile")
        ax.set_ylabel("Absorbed power $\\mathrm{[MW/m^{3}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        distributions_view.customize_legend(legend)

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plot_absorbed_power_density(
        self,
        ax,
        time_index,
    ):
        profiles = self.distributions_compute.get_profiles(time_index)

        if len(self.distributions_compute.active_distributions) != 0:
            ax.plot(
                self.distributions_compute.rho_tor_norm,
                profiles["all_injectors_total_power_density_profile"] * 1.0e-6,
                label=r"Electrons+Ions",
            )
            ax.plot(
                self.distributions_compute.rho_tor_norm,
                profiles["all_injectors_electron_power_density_profile"] * 1.0e-6,
                label=r"Electrons",
            )
            ax.plot(
                self.distributions_compute.rho_tor_norm,
                profiles["all_injectors_ion_power_density_profile"] * 1.0e-6,
                label=r"Ions",
            )
        ax.set_title("NBI/FUS power all injectors electrons ion profile")
        ax.set_ylabel("Absorbed power $\\mathrm{[MW/m^{3}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        distributions_view.customize_legend(legend)

    # CD PROFILE [MA/M2]
    def plot_c_d_profile(
        self,
        ax,
        time_index,
    ):
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_index)
        profiles = self.distributions_compute.get_profiles(time_index)

        if self.distributions_compute.cur_calc == 1:
            if len(self.distributions_compute.active_distributions) != 0:
                ax.plot(
                    self.distributions_compute.rho_tor_norm,
                    profiles["all_injectors_current_density_profile"] * 1.0e-6,
                    label="All Injectors",
                )
                for idistrib in range(self.distributions_compute.ndistributions):
                    if radial_grid_info[idistrib]["is_active"]:
                        lbl = ""
                        if idistrib == 0 or self.distributions_compute.ndistributions - 1 == idistrib:
                            lbl = profiles["single_nf_source_name"][idistrib]
                        ax.plot(
                            self.distributions_compute.rho_tor_norm,
                            profiles["single_total_power_density_profile"][idistrib] * 1.0e-6,
                            label=lbl,
                        )
        ax.set_ylabel("Current density $\\mathrm{[MA/m^{2}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")
        ax.set_title("NBI/FUS power profile")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        distributions_view.customize_legend(legend)

    # NBI/FUS POWER AND CD WAVEFORMS
    def plot_n_b_i_fus_power_and_c_d_waveforms(
        self,
        ax,
        time_index,
    ):
        time_array = self.ids.time
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_index)
        profiles = self.distributions_compute.get_profiles(time_index)

        if len(self.distributions_compute.active_distributions) != 0:
            ax.plot(
                time_array,
                np.array(profiles["all_injectors_total_power_waveform"]) * 1.0e-6,
                label=r"Total",
            )
            ax.plot(
                time_array,
                np.array(profiles["all_injectors_electron_power_waveform"]) * 1.0e-6,
                label=r"To electrons",
            )
            ax.plot(
                time_array,
                np.array(profiles["all_injectors_ion_power_waveform"]) * 1.0e-6,
                label=r"To ions",
            )
        for idistrib in range(self.distributions_compute.ndistributions):
            if radial_grid_info[idistrib]["is_active"]:
                lbl = ""
                if idistrib == 0 or self.distributions_compute.ndistributions - 1 == idistrib:
                    lbl = profiles["single_nf_source_name"][idistrib]
                # ax.plot(timeArray, np.array(profiles['single_total_power_waveform'][idistrib])*1.e-6,
                # label=profiles['single_nf_source_name'][idistrib])
                ax.plot(
                    time_array,
                    np.array(profiles["single_total_power_waveform"][idistrib]) * 1.0e-6,
                    label=lbl,
                )
        ax.set_ylabel("Power to the bulk $\\mathrm{[MW]}$")
        ax.set_xlabel("Time (s)")
        ax.set_title("NBI/FUS power waveform")
        if profiles is not None:
            ax.set_ylim(0, max(profiles["all_injectors_total_power_waveform"]) * 1.2e-6)
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        distributions_view.customize_legend(legend)

    # CD WAVEFORM
    def plot_c_d_waveform(
        self,
        ax,
        time_index,
    ):
        time_array = self.ids.time
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_index)

        profiles = self.distributions_compute.get_profiles(time_index)

        if self.distributions_compute.cur_calc == 1:
            if len(self.distributions_compute.active_distributions) != 0:
                ax.plot(
                    time_array,
                    np.array(profiles["all_injectors_current_waveform"]) * 1.0e-6,
                    label=r"Total",
                )
            for idistrib in range(self.distributions_compute.ndistributions):
                if radial_grid_info[idistrib]["is_active"]:
                    lbl = ""
                    if idistrib == 0 or self.distributions_compute.ndistributions - 1 == idistrib:
                        lbl = profiles["single_nf_source_name"][idistrib]
                    # ax.plot(timeArray, np.array(profiles['single_current_waveform'][idistrib])*1.e-6,label=
                    # profiles['single_nf_source_name'][idistrib])
                    ax.plot(
                        time_array,
                        np.array(profiles["single_current_waveform"][idistrib]) * 1.0e-6,
                        label=lbl,
                    )
            ax.set_ylabel("Current Drive $\\mathrm{[MA]}$")
            ax.set_xlabel("Time (s)")
            ax.set_title("NBI/FUS Current Density waveform")
            # ax.set_ylim(0,max(profiles['all_injectors_current_waveform'])*1.2e-3)
            legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            distributions_view.customize_legend(legend)
        else:
            ax.remove()

    @staticmethod
    def customize_legend(legend):
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(10)
        for label in legend.get_lines():
            label.set_linewidth(1.5)  # the legend line width
        return
