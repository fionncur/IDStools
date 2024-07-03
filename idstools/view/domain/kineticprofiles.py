import logging

import matplotlib.ticker as mtick

from idstools.domain.kineticprofiles import KineticProfilesCompute

logger = logging.getLogger("module")


class KineticProfilesView:
    single_style = "o"
    multi_style = "-"

    def __init__(self, connection, edgeRequired=False, timeSlice=-99.0):
        self.kProfiles = KineticProfilesCompute()
        self.kProfiles.analyze(connection, edgeRequired, timeSlice)
        if self.kProfiles.isCoreProfilesPresent:
            self.plotstyle = (
                KineticProfilesView.multi_style
                if len(self.kProfiles.waveform["time"]) > 1
                else KineticProfilesView.single_style
            )
        else:
            self.plotstyle = KineticProfilesView.single_style

    @staticmethod
    def customizeLegend(legend, facecolor="0.95", textFont=10, lineWidth=1.5):
        frame = legend.get_frame()
        frame.set_facecolor(facecolor)
        for label in legend.get_texts():
            label.set_fontsize(textFont)
        for label in legend.get_lines():
            label.set_linewidth(lineWidth)  # the legend line width
        return

    @staticmethod
    def viewTimeLine(ax, time):
        ymin = ax.get_ylim()[0]
        ymax = ax.get_ylim()[1]
        ax.plot(
            [time, time],
            [ymin, ymax],
            color="gray",
            linestyle="--",
            linewidth=2,
            label=r"$t_{slice}$",
        )
        ax.set_ylim(ymin, ymax)

    def viewCentralTemperatureWaveforms(self, ax):
        """
        This function plots central temperature waveforms with optional ion temperature

        Args:
            ax: a  matplotlib Axes object.
        """
        ax.plot(
            self.kProfiles.waveform["time"],
            self.kProfiles.waveform["te"]["central"],
            self.plotstyle,
            color="r",
            label=r"$T_e(0)$",
        )
        if self.kProfiles.ti_flag != 0:
            ax.plot(
                self.kProfiles.waveform["time"],
                self.kProfiles.waveform["ti"]["central"],
                self.plotstyle,
                color="b",
                label=r"$T_i(0)$",
            )
        if self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1] > self.kProfiles.commonTimeArray[0]:
            ax.set_xlim(
                self.kProfiles.commonTimeArray[0],
                self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1],
            )

        KineticProfilesView.viewTimeLine(ax, self.kProfiles.commonTime)
        ax.set_xlabel("$Time\/[\mathrm{s}]$")
        ax.set_ylabel("$T\/[\mathrm{keV}]$")
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)
        ax.set_title("Profiles displayed for t = " + "%.1f" % self.kProfiles.commonTime + " s")

    def viewCentralDensityWaveforms(self, ax, logscale=False):
        """
        This function plots various density waveforms over time

        Args:
            ax: a Matplotlib axis object.
        """
        ax.plot(
            self.kProfiles.waveform["time"],
            self.kProfiles.waveform["ne"]["central"],
            self.plotstyle,
            color="r",
            label=r"$n_e(0)$",
        )
        if max(self.kProfiles.nspec_over_ne) > 0:
            ax.plot(
                self.kProfiles.waveform["time"],
                self.kProfiles.waveform["ni"]["central"],
                self.plotstyle,
                color="b",
                label=r"$n_i(0)$",
            )
        for ispecies in range(self.kProfiles.nspeciesCore):
            if (self.kProfiles.isCompositionAvailable == 1) & (
                self.kProfiles.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT
            ):
                ax.plot(
                    self.kProfiles.waveform["time"],
                    self.kProfiles.waveform["n_species"][self.kProfiles.species[ispecies]]["density"]["central"],
                    self.plotstyle,
                    label=r"$n_{" + self.kProfiles.species[ispecies] + "}(0)$",
                )

        KineticProfilesView.viewTimeLine(ax, self.kProfiles.commonTime)
        ax.set_xlabel("$Time\/[\mathrm{s}]$")
        ax.set_ylabel("$n\/[\mathrm{m^{-3}}]$")

        if self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1] > self.kProfiles.commonTimeArray[0]:
            ax.set_xlim(
                self.kProfiles.commonTimeArray[0],
                self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1],
            )
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)
        if logscale:
            ax.set_yscale("log")

    def viewCentralZeffWaveform(self, ax):
        """
        This function plots the central Z-effective waveform over time.

        Args:
            ax: a Matplotlib axis object.
        """
        ax.plot(
            self.kProfiles.waveform["time"],
            self.kProfiles.waveform["zeff"]["central"],
            self.plotstyle,
            color="b",
            label=r"$Z_{eff}(0)$",
        )
        self.viewTimeLine(ax, self.kProfiles.commonTime)
        ax.set_xlabel(r"$Time\/[\mathrm{s}]$")
        ax.set_ylabel("$Z_{eff}$")
        if self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1] > self.kProfiles.commonTimeArray[0]:
            ax.set_xlim(
                self.kProfiles.commonTimeArray[0],
                self.kProfiles.commonTimeArray[self.kProfiles.commonTimeLength - 1],
            )
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)

    def viewTemperatureProfiles(self, ax):
        """
        This function plots temperature profiles for electron and ion temperatures at the core and edge regions based on the provided data.

        Args:
            ax: a matplotlib Axes object
        """
        if self.kProfiles.isCoreProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm"],
                self.kProfiles.profiles["te"],
                color="r",
                label=r"$T_e$",
            )
            if self.kProfiles.ti_flag != 0:
                ax.plot(
                    self.kProfiles.profiles["rhonorm"],
                    self.kProfiles.profiles["ti"],
                    color="b",
                    label=r"$T_i$",
                )
        if self.kProfiles.isEdgeProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm_e"],
                self.kProfiles.profiles["te_e"],
                color="r",
                label=r"$T_{e,edge}$",
            )
            ax.plot(
                self.kProfiles.profiles["rhonorm_e"],
                self.kProfiles.profiles["ti_e"],
                color="b",
                label=r"$T_{i,edge}$",
            )
        if not self.kProfiles.r_out_graph:
            ax.set_xlabel(r"$\rho/\rho_0$")
            ax.set_ylabel("$T\/[\mathrm{keV}]$")
        else:
            ax.set_xlabel(r"$R_{maj}\/[\mathrm{m}]$")
            ax.set_ylabel("$T\/[\mathrm{keV}]$")
        ax.set_xlim(self.kProfiles.xbeg, self.kProfiles.xend)
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set_title("t = " + "%.1f" % self.kProfiles.commonTime + " s")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)

    def viewDensityProfiles(self, ax, logscale=False):
        """
        This function plots density profiles for different species in a plasma based on provided kinetic profiles.

        Args:
            ax: a Matplotlib axis object
        """
        if self.kProfiles.isCoreProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm"],
                self.kProfiles.profiles["ne"],
                color="r",
                label=r"$n_e$",
            )
            if max(self.kProfiles.nspec_over_ne) > 0:
                ax.plot(
                    self.kProfiles.profiles["rhonorm"],
                    self.kProfiles.profiles["ni"],
                    color="b",
                    label=r"$n_i$",
                )
        if self.kProfiles.isEdgeProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm_e"],
                self.kProfiles.profiles["ne_e"],
                color="r",
                label=r"$n_{e,edge}$",
            )
            ax.plot(
                self.kProfiles.profiles["rhonorm_e"],
                self.kProfiles.profiles["ni_e"],
                color="b",
                label=r"$n_{i,edge}$",
            )
        for ispecies in range(self.kProfiles.nspeciesCore):
            if self.kProfiles.isCompositionAvailable and self.kProfiles.isCoreProfilesPresent:
                if self.kProfiles.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT:
                    ax.plot(
                        self.kProfiles.profiles["rhonorm"],
                        self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["density"],
                        label=r"$n_" + self.kProfiles.species[ispecies] + "$",
                    )
            if self.kProfiles.isEdgeProfilesPresent and self.kProfiles.species_map[ispecies] != -99:
                if (
                    self.kProfiles.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT
                    or self.kProfiles.isCoreProfilesPresent == 0
                ):
                    ax.plot(
                        self.kProfiles.profiles["rhonorm_e"],
                        self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["density_e"],
                        label=r"$n_{" + self.kProfiles.species[ispecies] + ",edge}$",
                    )
        if not self.kProfiles.r_out_graph:
            ax.set_xlabel(r"$\rho/\rho_0$")
            ax.set_ylabel("$n\/[\mathrm{m^{-3}}]$")
        else:
            ax.set_xlabel(r"$R_{maj}\/[\mathrm{m}]$")
            ax.set_ylabel("$n\/[\mathrm{m^{-3}}]$")
        if logscale:
            ax.set_yscale("log")
        ax.set_xlim(self.kProfiles.xbeg, self.kProfiles.xend)
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set_title("t = " + "%.1f" % self.kProfiles.commonTime + " s")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)

    def viewZeffProfile(self, ax):
        """
        This function plots Zeff profiles at the core and edge regions

        Args:
            ax: a Matplotlib axis object
        """
        if self.kProfiles.isCoreProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm"],
                self.kProfiles.profiles["zeff"],
                color="b",
                label=r"$Z_{eff}$",
            )
        if self.kProfiles.isEdgeProfilesPresent:
            ax.plot(
                self.kProfiles.profiles["rhonorm_e"],
                self.kProfiles.profiles["zeff_e"],
                color="b",
                label=r"$Z_{eff,edge}$",
            )
        if not self.kProfiles.r_out_graph:
            ax.set_xlabel(r"$\rho/\rho_0$")
            ax.set_ylabel("$Z_{eff}$")
        else:
            ax.set_xlabel(r"$R_{maj}\/[\mathrm{m}]$")
            ax.set_ylabel("$Z_{eff}$")
        ax.set_xlim(self.kProfiles.xbeg, self.kProfiles.xend)
        # ax.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        ax.set_title("t = " + "%.1f" % self.kProfiles.commonTime + " s")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        KineticProfilesView.customizeLegend(legend)

    def viewVtorProfile(self, ax, logscale=False):
        """
        This Python function plots the toroidal rotation velocity profiles for different species in a plasma simulation.

        Args:
            ax: a matplotlib axis object.
        """
        if (
            self.kProfiles.isCompositionAvailable
            and (self.kProfiles.vtor_flag != 0 or self.kProfiles.vtor_e_flag != 0)
            and (max(self.kProfiles.nspec_over_ne) > 0 or not self.kProfiles.isCoreProfilesPresent)
        ):
            for ispecies in range(self.kProfiles.nspeciesCore):
                if self.kProfiles.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT:
                    if "vtor" in self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]].keys():
                        if self.kProfiles.vtor_flag != 0:
                            ax.plot(
                                self.kProfiles.profiles["rhonorm"],
                                self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["vtor"],
                                label=r"$vtor_" + self.kProfiles.species[ispecies] + "$",
                            )
                        if (
                            self.kProfiles.isEdgeProfilesPresent
                            and self.kProfiles.species_map[ispecies] != -99
                            and self.kProfiles.vtor_e_flag != 0
                        ):
                            ax.plot(
                                self.kProfiles.profiles["rhonorm_e"],
                                self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["vtor_e"],
                                label=r"$vtor_{" + self.kProfiles.species[ispecies] + ",edge}$",
                            )
            if not self.kProfiles.r_out_graph:
                ax.set_xlabel(r"$\rho/\rho_0$")
                ax.set_ylabel(r"$|v_{tor}|\/[\mathrm{m.s^{-1}}]$")
            else:
                ax.set_xlabel(r"$R_{maj}\/[\mathrm{m}]$")
                ax.set_ylabel(r"$|v_{tor}|\/[\mathrm{m.s^{-1}}]$")
            ax.set_xlim(self.kProfiles.xbeg, self.kProfiles.xend)
            if logscale is False:
                if self.kProfiles.max_vtor > self.kProfiles.min_vtor:
                    ax.set_ylim(self.kProfiles.min_vtor, self.kProfiles.max_vtor * 1.1)

            ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            ax.set_title("t = " + "%.1f" % self.kProfiles.commonTime + " s")
            legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            KineticProfilesView.customizeLegend(legend)
            if logscale:
                ax.set_yscale("log")
        else:
            ax.remove()

    def viewVpolProfile(self, ax, logscale=False):
        """
        This function plots the vpol profiles for different species based on certain conditions and customizes the legend and axis labels accordingly.

        Args:
            ax: a matplotlib Axes object.
        """
        if (
            self.kProfiles.isCompositionAvailable
            and (self.kProfiles.vpol_flag != 0 or self.kProfiles.vpol_e_flag != 0)
            and (max(self.kProfiles.nspec_over_ne) > 0 or not self.kProfiles.isCoreProfilesPresent)
        ):
            for ispecies in range(self.kProfiles.nspeciesCore):
                if self.kProfiles.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT:
                    if "vpol" in self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]].keys():
                        if self.kProfiles.vpol_flag != 0:
                            ax.plot(
                                self.kProfiles.profiles["rhonorm"],
                                self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["vpol"],
                                label=r"$vpol_" + self.kProfiles.species[ispecies] + "$",
                            )
                        if (
                            self.kProfiles.isEdgeProfilesPresent
                            and self.kProfiles.species_map[ispecies] != -99
                            and self.kProfiles.vpol_e_flag != 0
                        ):
                            ax.plot(
                                self.kProfiles.profiles["rhonorm_e"],
                                self.kProfiles.profiles["n_species"][self.kProfiles.species[ispecies]]["vpol_e"],
                                label=r"$vpol_{" + self.kProfiles.species[ispecies] + ",edge}$",
                            )
            if not self.kProfiles.r_out_graph:
                ax.set_xlabel(r"$\rho/\rho_0$")
                ax.set_ylabel(r"$|v_{pol}|\/[\mathrm{m.s^{-1}}]$")
            else:
                ax.set_xlabel(r"$R_{maj}\/[\mathrm{m}]$")
                ax.set_ylabel(r"$|v_{pol}|\/[\mathrm{m.s^{-1}}]$")
            ax.set_xlim(self.kProfiles.xbeg, self.kProfiles.xend)
            if logscale is False:
                if self.kProfiles.max_vpol > self.kProfiles.min_vpol:
                    ax.set_ylim(self.kProfiles.min_vpol, self.kProfiles.max_vpol * 1.1)

            ax.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))
            ax.set_title("t = " + "%.1f" % self.kProfiles.commonTime + " s")
            legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
            KineticProfilesView.customizeLegend(legend)
            if logscale:
                ax.set_yscale("log")
        else:
            ax.remove()
