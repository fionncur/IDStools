import logging

import numpy as np

from idstools.compute.distributions import DistributionsCompute

logger = logging.getLogger(f"module.{__name__}")


class DistributionsView:
    def __init__(self, ids):
        self.distributionsCompute = DistributionsCompute(ids)
        self.ids = ids

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plotAbsorbedPowerDensityIndividual(
        self,
        ax,
        timeIndex,
    ):
        radialGridInfo = self.distributionsCompute.getRadialGridInfo(timeIndex)
        profiles = self.distributionsCompute.getProfiles(timeIndex)

        if len(self.distributionsCompute.activeDistributions) != 0:
            ax.plot(
                self.distributionsCompute.rho_tor_norm,
                profiles["all_injectors_total_power_density_profile"] * 1.0e-6,
                label=r"All injectors",
                color="black",
            )
            for idistrib in range(self.distributionsCompute.ndistributions):
                if radialGridInfo[idistrib]["is_active"]:
                    lbl = ""
                    if (
                        idistrib == 0
                        or self.distributionsCompute.ndistributions - 1 == idistrib
                    ):
                        lbl = profiles["single_nf_source_name"][idistrib]
                    # ax.plot(self.distributionsCompute.rho_tor_norm, profiles['single_total_power_density_profile'][idistrib]*1.e-6,label=profiles['single_nf_source_name'][idistrib])
                    ax.plot(
                        self.distributionsCompute.rho_tor_norm,
                        profiles["single_total_power_density_profile"][idistrib]
                        * 1.0e-6,
                        label=lbl,
                    )
        ax.set_title("NBI/FUS power individual injectors profile")
        ax.set_ylabel("Absorbed power $\mathrm{[MW/m^{3}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        DistributionsView.customizeLegend(legend)

    # PROFILE OF ABSORBED POWER DENSITY ON ELECTRONS+IONS FOR ALL INJECTORS AND EACH OF THEM INDIVIDUALLY [MW/M3]
    def plotAbsorbedPowerDensity(
        self,
        ax,
        timeIndex,
    ):
        radialGridInfo = self.distributionsCompute.getRadialGridInfo(timeIndex)
        profiles = self.distributionsCompute.getProfiles(timeIndex)

        if len(self.distributionsCompute.activeDistributions) != 0:
            ax.plot(
                self.distributionsCompute.rho_tor_norm,
                profiles["all_injectors_total_power_density_profile"] * 1.0e-6,
                label=r"Electrons+Ions",
            )
            ax.plot(
                self.distributionsCompute.rho_tor_norm,
                profiles["all_injectors_electron_power_density_profile"] * 1.0e-6,
                label=r"Electrons",
            )
            ax.plot(
                self.distributionsCompute.rho_tor_norm,
                profiles["all_injectors_ion_power_density_profile"] * 1.0e-6,
                label=r"Ions",
            )
        ax.set_title("NBI/FUS power all injectors electrons ion profile")
        ax.set_ylabel("Absorbed power $\mathrm{[MW/m^{3}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        DistributionsView.customizeLegend(legend)

    # CD PROFILE [MA/M2]
    def plotCDProfile(
        self,
        ax,
        timeIndex,
    ):
        radialGridInfo = self.distributionsCompute.getRadialGridInfo(timeIndex)
        profiles = self.distributionsCompute.getProfiles(timeIndex)

        if self.distributionsCompute.cur_calc == 1:
            if len(self.distributionsCompute.activeDistributions) != 0:
                ax.plot(
                    self.distributionsCompute.rho_tor_norm,
                    profiles["all_injectors_current_density_profile"] * 1.0e-6,
                    label="All Injectors",
                )
                for idistrib in range(self.distributionsCompute.ndistributions):
                    if radialGridInfo[idistrib]["is_active"]:
                        lbl = ""
                        if (
                            idistrib == 0
                            or self.distributionsCompute.ndistributions - 1 == idistrib
                        ):
                            lbl = profiles["single_nf_source_name"][idistrib]
                        ax.plot(
                            self.distributionsCompute.rho_tor_norm,
                            profiles["single_total_power_density_profile"][idistrib]
                            * 1.0e-6,
                            label=lbl,
                        )
        ax.set_ylabel("Current density $\mathrm{[MA/m^{2}]}$")
        ax.set_xlabel("Normalized toroidal flux coordinate")
        ax.set_title("NBI/FUS power profile")

        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        DistributionsView.customizeLegend(legend)

    # NBI/FUS POWER AND CD WAVEFORMS
    def plotNBIFusPowerAndCDWaveforms(
        self,
        ax,
        timeIndex,
    ):
        timeArray = self.ids.time
        radialGridInfo = self.distributionsCompute.getRadialGridInfo(timeIndex)
        profiles = self.distributionsCompute.getProfiles(timeIndex)

        if len(self.distributionsCompute.activeDistributions) != 0:
            ax.plot(
                timeArray,
                np.array(profiles["all_injectors_total_power_waveform"]) * 1.0e-6,
                label=r"Total",
            )
            ax.plot(
                timeArray,
                np.array(profiles["all_injectors_electron_power_waveform"]) * 1.0e-6,
                label=r"To electrons",
            )
            ax.plot(
                timeArray,
                np.array(profiles["all_injectors_ion_power_waveform"]) * 1.0e-6,
                label=r"To ions",
            )
        for idistrib in range(self.distributionsCompute.ndistributions):
            if radialGridInfo[idistrib]["is_active"]:
                lbl = ""
                if (
                    idistrib == 0
                    or self.distributionsCompute.ndistributions - 1 == idistrib
                ):
                    lbl = profiles["single_nf_source_name"][idistrib]
                # ax.plot(timeArray, np.array(profiles['single_total_power_waveform'][idistrib])*1.e-6,label=profiles['single_nf_source_name'][idistrib])
                ax.plot(
                    timeArray,
                    np.array(profiles["single_total_power_waveform"][idistrib])
                    * 1.0e-6,
                    label=lbl,
                )
        ax.set_ylabel("Power to the bulk $\mathrm{[MW]}$")
        ax.set_xlabel("Time (s)")
        ax.set_title("NBI/FUS power waveform")
        ax.set_ylim(0, max(profiles["all_injectors_total_power_waveform"]) * 1.2e-6)
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        DistributionsView.customizeLegend(legend)

    # CD WAVEFORM
    def plotCDWaveform(
        self,
        ax,
        timeIndex,
    ):
        timeArray = self.ids.time
        radialGridInfo = self.distributionsCompute.getRadialGridInfo(timeIndex)

        profiles = self.distributionsCompute.getProfiles(timeIndex)

        if self.distributionsCompute.cur_calc == 1:
            if len(self.distributionsCompute.activeDistributions) != 0:
                ax.plot(
                    timeArray,
                    np.array(profiles["all_injectors_current_waveform"]) * 1.0e-6,
                    label=r"Total",
                )
            for idistrib in range(self.distributionsCompute.ndistributions):
                if radialGridInfo[idistrib]["is_active"]:
                    lbl = ""
                    if (
                        idistrib == 0
                        or self.distributionsCompute.ndistributions - 1 == idistrib
                    ):
                        lbl = profiles["single_nf_source_name"][idistrib]
                    # ax.plot(timeArray, np.array(profiles['single_current_waveform'][idistrib])*1.e-6,label=profiles['single_nf_source_name'][idistrib])
                    ax.plot(
                        timeArray,
                        np.array(profiles["single_current_waveform"][idistrib])
                        * 1.0e-6,
                        label=lbl,
                    )
            ax.set_ylabel("Current Drive $\mathrm{[MA]}$")
            ax.set_xlabel("Time (s)")
            ax.set_title("NBI/FUS Current Density waveform")
            # ax.set_ylim(0,max(profiles['all_injectors_current_waveform'])*1.2e-3)
            legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            DistributionsView.customizeLegend(legend)
        else:
            ax.remove()

    @staticmethod
    def customizeLegend(legend):
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(10)
        for label in legend.get_lines():
            label.set_linewidth(1.5)  # the legend line width
        return
