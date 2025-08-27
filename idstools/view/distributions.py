import logging

import numpy as np

from idstools.compute.distributions import DistributionsCompute

logger = logging.getLogger(f"module.{__name__}")


class DistributionsView:
    def __init__(self, ids):
        self.distributions_compute = DistributionsCompute(ids)
        self.ids = ids

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plot_absorbed_power_density_individual(
        self,
        ax,
        time_slice,
    ):
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_slice)
        profiles = self.distributions_compute.get_profiles(time_slice)

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

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plot_absorbed_power_density(
        self,
        ax,
        time_slice,
    ):
        profiles = self.distributions_compute.get_profiles(time_slice)

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

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # CD PROFILE [MA/M2]
    def plot_cd_profile(
        self,
        ax,
        time_slice,
    ):
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_slice)
        profiles = self.distributions_compute.get_profiles(time_slice)

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

        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # NBI/FUS POWER AND CD WAVEFORMS
    def plot_nbi_fus_power_and_cd_waveforms(
        self,
        ax,
        time_slice,
    ):
        time_array = self.ids.time
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_slice)
        profiles = self.distributions_compute.get_profiles(time_slice)

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
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # CD WAVEFORM
    def plot_cd_waveform(
        self,
        ax,
        time_slice,
    ):
        time_array = self.ids.time
        radial_grid_info = self.distributions_compute.get_radial_grid_info(time_slice)

        profiles = self.distributions_compute.get_profiles(time_slice)

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
            ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        else:
            ax.remove()
