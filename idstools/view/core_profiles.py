# plot_ne0 and plot density profile function
# not ok src/view/core_profiles/functions.py
import logging
import numpy as np
from idstools.compute.core_profiles import CoreProfilesCompute
from idstools.view.common import Console

logger = logging.getLogger("module")


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
        print("---------------")
        print("core_profiles")
        print("---------------")
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
        disp_species = f"{'species:': <15}"
        disp_a = f"{'a:': <15}"
        disp_z = f"{'z:': <15}"
        disp_nspec_over_ntot = f"{'n_over_ntot:': <15}"
        disp_nspec_over_ne = f"{'n_over_ne:': <15}"
        disp_nspec_over_nmaj = f"{'n_over_n_maj:': <15}"
        main_species = ""

        for species_key, species_data in composition_data.items():
            if species_data["nspec_over_ntot"] > 0.45:
                if len(main_species) == 0:
                    main_species = main_species + species_data["species"]
                else:
                    main_species = main_species + "-" + species_data["species"]
            if species_data["nspec_over_ne"] > 0.0:
                species_name = f"{species_data['species']}({species_data['label']})"
                species_name = species_name[:11]
                disp_species = f"{disp_species} {species_name : >12}"
                a = f"{species_data['a'] :.1f}"
                disp_a = f"{disp_a} {a : >12}"
                z = f"{species_data['z'] :.1f}"
                disp_z = f"{disp_z} {z : >12}"
                if species_data["nspec_over_ntot"] < 1.0e-2:
                    nspec_over_ntot = f"{species_data['nspec_over_ntot'] :.2e}"
                    disp_nspec_over_ntot = (
                        f"{disp_nspec_over_ntot} {nspec_over_ntot : >12}"
                    )
                else:
                    nspec_over_ntot = f"{species_data['nspec_over_ntot'] :.3f}"
                    disp_nspec_over_ntot = (
                        f"{disp_nspec_over_ntot} {nspec_over_ntot : >12}"
                    )
                if species_data["nspec_over_ne"] < 1.0e-2:
                    nspec_over_ne = f"{species_data['nspec_over_ne'] :.2e}"
                    disp_nspec_over_ne = f"{disp_nspec_over_ne} {nspec_over_ne : >12}"
                else:
                    nspec_over_ne = f"{species_data['nspec_over_ne'] :.3f}"
                    disp_nspec_over_ne = f"{disp_nspec_over_ne} {nspec_over_ne : >12}"
                if species_data["nspec_over_nmaj"] < 1.0e-2:
                    nspec_over_nmaj = f"{species_data['nspec_over_nmaj'] :.2e}"
                    disp_nspec_over_nmaj = (
                        f"{disp_nspec_over_nmaj} {nspec_over_nmaj : >12}"
                    )
                else:
                    nspec_over_nmaj = f"{species_data['nspec_over_nmaj'] :.3f}"
                    disp_nspec_over_nmaj = (
                        f"{disp_nspec_over_nmaj} {nspec_over_nmaj : >12}"
                    )

        print(disp_species)
        print(disp_a)
        print(disp_z)
        print(disp_nspec_over_ntot)
        print(disp_nspec_over_ne)
        print(disp_nspec_over_nmaj)
        print("-----------------------")

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
                    print(f"{species_data['species']} has {nstates} state{comm}")
                istate = 0
                for state_key, state_data in states.items():
                    if state_data["density_available"] is False:
                        print(
                            f"\t!  core_profile IDS: Density is not available for state {istate + 1}"
                        )
                    else:
                        n_ni = f"{state_data['n_ni']:.6f}"
                        label_space = 0
                        if state_data["label"].strip() != "":
                            label_space = 7
                        print(
                            f"\t {'state' +str(istate + 1) : <8}{state_data['label']: <{label_space}}z : {state_data['z_average']: <10} n/ni, % :{n_ni : >12}"
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

    def plotIonPressureProperties(self, ax):
        FACTOR = 1.0e-6
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            logger.critical("----> Aborted.")
            return

        volume = self.coreProfilesCompute.getVolume()  # Volume profile (not mandatory)

        dictIonPressureProperties = self.coreProfilesCompute.getIonPressureProperties()
        maximaIon = dictIonPressureProperties["maximaIon"]
        pressureIonThermal = dictIonPressureProperties["pressureIonThermal"]
        pressureIonFastParallel = dictIonPressureProperties["pressureIonFastParallel"]
        pressureIonFastPerpendicular = dictIonPressureProperties[
            "pressureIonFastPerpendicular"
        ]

        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }

        ax.plot(rhoTorNorm, pressureIonThermal * FACTOR, label="Thermal ion")
        ax.plot(rhoTorNorm, pressureIonFastParallel * FACTOR, label="Fast parallel ion")
        ax.plot(
            rhoTorNorm,
            pressureIonFastPerpendicular * FACTOR,
            label="Fast perpendicular ion",
        )
        ax.set_ylim(0, maximaIon * FACTOR)
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"P (MPa)", fontArgs, labelpad=0)
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.4, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Ion Pressure Properties", loc="left")

    def showInfoOnPlot(self, ax, info: str = "", location="right"):
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
        if location == "top":
            ax.text(
                xmin,
                ymax + 0.2,
                info,
                horizontalalignment="left",
                rotation="horizontal",
                fontsize=5,
            )
        else:
            ax.text(
                xmax + 0.01 * abs(xmax),
                ymin + 0.01 * abs(ymax - ymin),
                info,
                horizontalalignment="left",
                verticalalignment="center",
                rotation="vertical",
                fontsize=5,
            )

    def plotElectronPressureProperties(self, ax, **kwargs):
        FACTOR = 1.0e-6
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            logger.critical("----> Aborted.")

        dictElectronsPressureProperties = (
            self.coreProfilesCompute.getElectronsPressureProperties()
        )
        maximaElectrons = dictElectronsPressureProperties["maximaElectrons"]
        pressureElectronTotal = dictElectronsPressureProperties["pressureElectronTotal"]
        pressureElectronThermal = dictElectronsPressureProperties[
            "pressureElectronThermal"
        ]
        pressureElectronFastParallel = dictElectronsPressureProperties[
            "pressureElectronFastParallel"
        ]
        pressureElectronFastPerpendicular = dictElectronsPressureProperties[
            "pressureElectronFastPerpendicular"
        ]
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.plot(rhoTorNorm, pressureElectronTotal * FACTOR, label="Total electron")
        ax.plot(rhoTorNorm, pressureElectronThermal * FACTOR, label="Thermal electron")
        ax.plot(
            rhoTorNorm,
            pressureElectronFastParallel * FACTOR,
            label="Fast parallel electron",
        )
        ax.plot(
            rhoTorNorm,
            pressureElectronFastPerpendicular * FACTOR,
            label="Fast perpendicular electron",
        )
        ax.set_ylim(0, maximaElectrons * FACTOR)

        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"P (MPa)", fontArgs, labelpad=0)
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.5, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Electrons Pressure Properties", loc="left")

    def plotTotalPressureProperties(self, ax, **kwargs):
        FACTOR = 1.0e-6
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            return

        dictPressure = self.coreProfilesCompute.getPressure()
        maximaTotal = dictPressure["maximaTotal"]
        pressureTotal = dictPressure["pressureTotal"]
        pressureThermal = dictPressure["pressureThermal"]
        pressureParallel = dictPressure["pressureParallel"]
        pressurePerpendicular = dictPressure["pressurePerpendicular"]

        if maximaTotal == 0:
            logger.critical("No pressure profile found")
            return
        ax.plot(rhoTorNorm, pressureTotal * FACTOR, label="Total")
        ax.plot(rhoTorNorm, pressureThermal * FACTOR, label="Thermal")
        ax.plot(rhoTorNorm, pressureParallel * FACTOR, label="Parallel")
        ax.plot(rhoTorNorm, pressurePerpendicular * FACTOR, label="Perpendicular")
        ax.set_xlim(rhoTorNorm[0], rhoTorNorm[nrho - 1])
        ax.set_ylim(0, maximaTotal * FACTOR)

        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"P (MPa)", fontArgs, labelpad=0)
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Total Pressure Properties", loc="left")

<<<<<<< HEAD
    def viewQProfileAndMagneticShearProfile(self, ax, **kwargs):
        """
        The function `viewQProfileAndMagneticShearProfile` plots the q-profile and magnetic shear profile using the given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which the plot will be drawn.
        """
        profiles = self.coreProfilesCompute.getProfiles()

        # q-profile and magnetic shear profile
        ax.plot(profiles["rhonorm"], profiles["q"], label=r"$q$")
        ax.plot(
            profiles["rhonorm"],
            profiles["magnetic_shear"],
            label=r"$s=\frac{1}{q}\frac{dq}{d\rho}$",
        )

        ax.set_ylabel(r"$q,\/s$")
        ax.set_xlim(0, 1)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    # Current density profiles

    def viewCurrentDesnityProfiles(self, ax, **kwargs):
        """
        The function `viewCurrentDesnityProfiles` plots various current density profiles on a given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes on which the plot will be drawn.
        """
        profiles = self.coreProfilesCompute.getProfiles()
        ax.plot(profiles["rhonorm"], profiles["j_total"] * 1.0e-3, label=r"$j_{TOT}$")
        ax.plot(
            profiles["rhonorm"], profiles["j_non_inductive"] * 1.0e-3, label=r"$j_{NI}$"
        )
        ax.plot(
            profiles["rhonorm"], profiles["j_bootstrap"] * 1.0e-3, label=r"$j_{BOOT}$"
        )
        ax.plot(profiles["rhonorm"], profiles["j_ohmic"] * 1.0e-3, label=r"$j_{OHM}$")

        ax.set_xlabel(r"$\rho/\rho_0$")
        ax.set_ylabel(r"$j\/[\mathrm{kA/m^2}]$")
        ax.set_xlim(0, 1)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
=======

    def plotEfieldProfile(self, ax, **kwargs):
        FACTOR = 1.e-3
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            return
        if len(self.ids.profiles_1d[0].e_field.radial) < 1:
            logger.critical('core_profiles.profiles_1d[0].e_field.radial could not be read')
            self.ids.profiles_1d[0].e_field.radial = np.asarray([np.nan]*nrho)
        ax.plot(rhoTorNorm,self.ids.profiles_1d[0].e_field.radial*FACTOR,label = "E-field")
        ax.set_xlim(rhoTorNorm[0],rhoTorNorm[nrho-1])

        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"E-field ($kV/m$)", fontArgs, labelpad=0)
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Electric field profile", loc="left")

    def plotToroidalVelocityProfile(self, ax, **kwargs):
        FACTOR = 1.e-3
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            return
        
        nions = len(self.ids.profiles_1d[0].ion)
        species = self.coreProfilesCompute.getSpecies(0)
        for ionIndex in range(nions):
            if len(self.ids.profiles_1d[0].ion[ionIndex].velocity.toroidal) < 1:
                logger.critical(f'core_profiles.profiles_1d[0].ion[{ionIndex}].velocity.toroidal could not be read')
                self.ids.profiles_1d[0].ion[ionIndex].velocity.toroidal = np.asarray([np.nan]*nrho)
            ax.plot(rhoTorNorm,self.ids.profiles_1d[0].ion[ionIndex].velocity.toroidal*FACTOR,label = species[ionIndex])
            
        ax.set_xlim(rhoTorNorm[0],rhoTorNorm[nrho-1])

        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"$v_{tor}$ ($km/s$)", fontArgs, labelpad=0)
        #TODO update
        # ax2.yaxis.tick_right()
        # ax2.yaxis.set_label_position("right")
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Toroidal velocity profile", loc="left")
        
    def plotPoloidalVelocityProfile(self, ax, **kwargs):
        FACTOR = 1.e-3
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            return
        
        nions = len(self.ids.profiles_1d[0].ion)
        species = self.coreProfilesCompute.getSpecies(0)
        for ionIndex in range(nions):
            if len(self.ids.profiles_1d[0].ion[ionIndex].velocity.poloidal) < 1:
                logger.critical(f'core_profiles.profiles_1d[0].ion[{ionIndex}].velocity.poloidal could not be read')
                self.ids.profiles_1d[0].ion[ionIndex].velocity.poloidal = np.asarray([np.nan]*nrho)
            ax.plot(rhoTorNorm,self.ids.profiles_1d[0].ion[ionIndex].velocity.poloidal*FACTOR,label = species[ionIndex])
            
        ax.set_xlim(rhoTorNorm[0],rhoTorNorm[nrho-1])

        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"$v_{pol}$ ($km/s$)", fontArgs, labelpad=0)
  
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title("Poloidal velocity profile", loc="left")
        
        
    def plotDiamagneticVelocityProfile(self, ax, **kwargs):
        FACTOR = 1.e-3
        rhoTorNorm = self.coreProfilesCompute.getRhoTorNorm()  # Rho profile (mandatory)
        nrho = len(rhoTorNorm)
        if nrho == 0:
            logger.critical(
                "core_profiles.profiles_1d[0].grid.rho_tor/core_profiles.profiles_1d[0].grid.rho_tor_norm) is empty",
            )
            return
        
        nions = len(self.ids.profiles_1d[0].ion)
        species = self.coreProfilesCompute.getSpecies(0)
        for ionIndex in range(nions):
            if len(self.ids.profiles_1d[0].ion[ionIndex].velocity.diamagnetic) < 1:
                logger.critical(f'core_profiles.profiles_1d[0].ion[{ionIndex}].velocity.diamagnetic could not be read')
                self.ids.profiles_1d[0].ion[ionIndex].velocity.diamagnetic = np.asarray([np.nan]*nrho)
            ax.plot(rhoTorNorm,self.ids.profiles_1d[0].ion[ionIndex].velocity.diamagnetic*FACTOR,label = species[ionIndex])
            
        ax.set_xlim(rhoTorNorm[0],rhoTorNorm[nrho-1])
        # ax4.yaxis.tick_right()
        # ax4.yaxis.set_label_position("right")
        # Set Plot properties
        fontArgs = {
            "fontfamily": "serif",
            "color": "darkred",
            "fontweight": "normal",
            "fontsize": 12,
        }
        ax.tick_params(
            which="both",
            labelsize=12,
        )
        ax.set_xlabel(r"$\rho/\rho_0$", fontArgs, labelpad=1)
        ax.set_ylabel(r"$v_{dia}$ ($km/s$)", fontArgs, labelpad=0)

        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        legend = ax.legend(
            loc="upper right"
        )  # bbox_to_anchor=(legx_pos - 0.35, legy_pos - 0.05)
        frame = legend.get_frame()
        frame.set_facecolor("0.95")
        for label in legend.get_texts():
            label.set_fontsize(7)
        for label in legend.get_lines():
            label.set_linewidth(1.5)
        ax.set_title(f"Diamagnetic velocity profile", loc="left")
>>>>>>> 00469b20748aba39ccb47b68e09fc065bd66ec9f
