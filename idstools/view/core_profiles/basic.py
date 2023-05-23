# plot_ne0 and plot density profile function
# not ok src/view/core_profiles/functions.py

from ...compute.core_profiles.basic import CoreProfilesCompute
from ...view.common.basic import Console


class CoreProfilesView(Console):
    def __init__(self, ids):
        self.ids = ids
        self.coreProfilesCompute = CoreProfilesCompute(ids)

    @staticmethod
    def view_plasma_composition_with_species_concentration(
        ids_object, slice_index=0, print_data=False, volume=None
    ):
        """
        Nice display of plasma composition with species concentrations
        """
        print("   ------------")
        print("core_profiles")
        print("   ------------")
        composition_data = (
            CoreProfilesCompute.getPlasmaCompositionWithSpeciesConcentration(
                ids_object, slice_index, volume=volume
            )
        )
        if composition_data != 0 and composition_data != -1:
            coreProfilesView = CoreProfilesView(ids_object)
            coreProfilesView._print_plasma_composition(composition_data)
            coreProfilesView._print_specis_concentration(composition_data)

            if print_data is True:
                import json

                print(json.dumps(composition_data, sort_keys=True, indent=4))

        return composition_data

    def _print_plasma_composition(self, composition_data):
        disp_species = "   species:      "
        disp_a = "   a:            "
        disp_z = "   z:            "
        disp_nspec_over_ntot = "   n_over_ntot:  "
        disp_nspec_over_ne = "   n_over_ne:    "
        disp_nspec_over_nmaj = "   n_over_n_maj: "
        main_species = ""

        for species_key, species_data in composition_data.items():
            if species_data["nspec_over_ntot"] > 0.45:
                if len(main_species) == 0:
                    main_species = main_species + species_data["species"]
                else:
                    main_species = main_species + "-" + species_data["species"]
            if species_data["nspec_over_ne"] > 0.0:
                disp_species = (
                    disp_species
                    + species_data["species"]
                    + " ("
                    + species_data["label"]
                    + ")"
                    + " "
                    * (
                        self.tabsize
                        - len(
                            species_data["species"] + " (" + species_data["label"] + ")"
                        )
                    )
                )
                disp_a = (
                    disp_a
                    + format("%.1f" % species_data["a"])
                    + " " * (self.tabsize - len(format("%.1f" % species_data["a"])))
                )
                disp_z = (
                    disp_z
                    + format("%.1f" % species_data["z"])
                    + " " * (self.tabsize - len(format("%.1f" % species_data["z"])))
                )
                if species_data["nspec_over_ntot"] < 1.0e-2:
                    disp_nspec_over_ntot = (
                        disp_nspec_over_ntot
                        + format("%.2e" % species_data["nspec_over_ntot"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.2e" % species_data["nspec_over_ntot"]))
                        )
                    )
                else:
                    disp_nspec_over_ntot = (
                        disp_nspec_over_ntot
                        + format("%.3f" % species_data["nspec_over_ntot"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.3f" % species_data["nspec_over_ntot"]))
                        )
                    )
                if species_data["nspec_over_ne"] < 1.0e-2:
                    disp_nspec_over_ne = (
                        disp_nspec_over_ne
                        + format("%.2e" % species_data["nspec_over_ne"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.2e" % species_data["nspec_over_ne"]))
                        )
                    )
                else:
                    disp_nspec_over_ne = (
                        disp_nspec_over_ne
                        + format("%.3f" % species_data["nspec_over_ne"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.3f" % species_data["nspec_over_ne"]))
                        )
                    )
                if species_data["nspec_over_nmaj"] < 1.0e-2:
                    disp_nspec_over_nmaj = (
                        disp_nspec_over_nmaj
                        + format("%.2e" % species_data["nspec_over_nmaj"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.2e" % species_data["nspec_over_nmaj"]))
                        )
                    )
                else:
                    disp_nspec_over_nmaj = (
                        disp_nspec_over_nmaj
                        + format("%.3f" % species_data["nspec_over_nmaj"])
                        + " "
                        * (
                            self.tabsize
                            - len(format("%.3f" % species_data["nspec_over_nmaj"]))
                        )
                    )

        print(disp_species)
        print(disp_a)
        print(disp_z)
        print(disp_nspec_over_ntot)
        print(disp_nspec_over_ne)
        print(disp_nspec_over_nmaj)
        print("   ------------")

    def _print_specis_concentration(self, composition_data):
        """
        This function prints information about the concentration of species and their states.

        Args:
            composition_data: The parameter composition_data is a dictionary containing information about
        the composition of a plasma, including the species present and their states.
        """
        for species_key, species_data in composition_data.items():
            states = species_data["states"]
            nstates = len(states)
            if nstates != 0:
                if nstates > 1:
                    comm = "s"
                else:
                    comm = ""
                if nstates != 0:
                    print(
                        species_data["species"],
                        " has ",
                        nstates,
                        " state" + comm,
                    )
                istate = 0
                for state_key, state_data in states.items():
                    if state_data["density_available"] is False:
                        print(
                            self.TAB,
                            "!  core_profile IDS: Density is not available for state ",
                            str(istate + 1),
                        )
                    else:
                        print(
                            self.TAB,
                            "state ",
                            str(istate + 1),
                            (" " * (5 - len(str(istate + 1)))),
                            state_data["label"],
                            (" " * (7 - len(str(state_data["label"])))),
                            "z =",
                            state_data["z_average"],
                            (" " * (7 - len(str(state_data["z_average"])))),
                            "   n/ni, % :",
                            format("%.6f" % (state_data["n_ni"])),
                        )
                    istate = istate + 1

    def plotElectronDensityNe0(self, ax):
        """
        This function plots the electron density (ne0) as a function of time.

        Args:
            ax: The parameter "ax" is a matplotlib axis object, which is used to plot the electron density data.
        """
        ne0 = self.coreProfilesCompute.getElectronDensityNe0()
        time_array = self.ids.time

        ax.plot(time_array, ne0, color="r", label="$n_{e0} [10^{19}.m^{-3}]$")

        ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(ip)*1.2)
        ax.set_ylim(0, 20)

    def plotDensityProfile(self, ax, timeIndex, psiCordinate=False, update=True):
        """
        This function plots the electron density profile as a function of either the normalized toroidal flux coordinate or the poloidal magnetic flux coordinate.

        Args:
            ax: ax is a matplotlib axis object where the density profile plot will be drawn.
            timeIndex: The time index refers to the specific time step or snapshot of data that is being plotted. It is used to retrieve the electron density and other relevant data at that particular
        time.
            psiCordinate: A boolean parameter that determines whether the density profile should be plotted as a function of the poloidal flux coordinate (-psi) or the normalised toroidal flux coordinate (rho_tor). If psiCordinate is True, the density profile will be plotted as a function of -psi. Defaults to False
            update: The `update` parameter is a boolean flag that determines whether the plot should be updated or created from scratch. If `update` is `True`, the function will create a new plot with the given data. If `update` is `False`, the function will update an existing plot with the new. Defaults to True

        Returns:
            a tuple containing the matplotlib plot object for the electron density profile (ax_density_plot_dens) and the maximum electron density value (nmax).
        """
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm(timeIndex)
        if rhoTorNorm is not None:
            radial_coordinate = rhoTorNorm
            xlabel = ""
            if update == True:
                xlabel = r"Normalised $\rho_{tor}$ [-]"
            if psiCordinate == True:
                psi = self.coreProfilesCompute.getPSI(timeIndex)
                if psi is not None:
                    radial_coordinate = psi
                    if update == True:
                        xlabel = r"$-\psi$ [Wb]"

            ax.set_xlabel(xlabel)
            electronDensity = self.ids.profiles_1d[timeIndex].electrons.density
            nmax = max(electronDensity) * 1.2
            ax_density_plot_dens = None
            if update == True:
                (ax_density_plot_dens,) = ax.plot(
                    radial_coordinate,
                    electronDensity,
                    color="b",
                    label=r"$n_e [m^{-3}]$",
                )
                # ax_density.set_ylim(bottom=0,top=max(electron_density))
            else:
                ax.legend(loc="upper right", shadow=True, fancybox=True)
                ax.set_ylim(top=nmax)
                ax.set_data(radial_coordinate, electronDensity)
            return ax_density_plot_dens, nmax
