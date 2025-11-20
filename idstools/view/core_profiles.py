# plot_ne0 and plot density profile function
# not ok src/view/core_profiles/functions.py
import logging

import numpy as np

from idstools.compute.core_profiles import CoreProfilesCompute

logger = logging.getLogger("module")


class CoreProfilesView:
    def __init__(self, ids):
        self.ids = ids
        self.core_profiles_compute = CoreProfilesCompute(ids)

    @staticmethod
    def view_plasma_composition_with_species_concentration(ids_object, time_slice, print_data=False, volume=None):
        """
        Nice display of plasma composition with species concentrations
        """
        print("---------------")
        print("core_profiles")
        print("---------------")
        composition_data = CoreProfilesCompute.get_plasma_composition_with_species_concentration(
            ids_object, time_slice, volume=volume
        )
        if composition_data != 0 and composition_data != -1:
            core_profiles_view = CoreProfilesView(ids_object)
            core_profiles_view._print_plasma_composition(composition_data)
            core_profiles_view._print_specis_concentration(composition_data)

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
                a = f"{species_data['a'].value :.1f}"
                disp_a = f"{disp_a} {a : >12}"
                z = f"{species_data['z'] :.1f}"
                disp_z = f"{disp_z} {z : >12}"
                if species_data["nspec_over_ntot"] < 1.0e-2:
                    nspec_over_ntot = f"{species_data['nspec_over_ntot'] :.2e}"
                    disp_nspec_over_ntot = f"{disp_nspec_over_ntot} {nspec_over_ntot : >12}"
                else:
                    nspec_over_ntot = f"{species_data['nspec_over_ntot'] :.3f}"
                    disp_nspec_over_ntot = f"{disp_nspec_over_ntot} {nspec_over_ntot : >12}"
                if species_data["nspec_over_ne"] < 1.0e-2:
                    nspec_over_ne = f"{species_data['nspec_over_ne'] :.2e}"
                    disp_nspec_over_ne = f"{disp_nspec_over_ne} {nspec_over_ne : >12}"
                else:
                    nspec_over_ne = f"{species_data['nspec_over_ne'] :.3f}"
                    disp_nspec_over_ne = f"{disp_nspec_over_ne} {nspec_over_ne : >12}"
                if species_data["nspec_over_nmaj"] < 1.0e-2:
                    nspec_over_nmaj = f"{species_data['nspec_over_nmaj'] :.2e}"
                    disp_nspec_over_nmaj = f"{disp_nspec_over_nmaj} {nspec_over_nmaj : >12}"
                else:
                    nspec_over_nmaj = f"{species_data['nspec_over_nmaj'] :.3f}"
                    disp_nspec_over_nmaj = f"{disp_nspec_over_nmaj} {nspec_over_nmaj : >12}"

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
                        print(f"\t!  core_profile IDS: Density is not available for state {istate + 1}")
                    else:
                        n_ni = f"{state_data['n_ni']:.6f}"
                        label_space = 0
                        if state_data["label"].strip() != "":
                            label_space = 7
                        print(
                            f"\t {'state' + str(istate + 1) : <8}{state_data['label'].value: <{label_space}}z : "
                            f"{state_data['z_average']: <10} n/ni, % :{n_ni : >12}"
                        )
                    istate = istate + 1

    def plot_electron_density_ne0(self, ax):
        """
        This function plots the electron density (ne0) as a function of time.

        Args:
            ax: The parameter "ax" is a matplotlib axis object, which is used to plot the electron density data.
        """
        ne0 = self.core_profiles_compute.get_electron_density_ne0()

        time_array = self.ids.time
        if len(ne0) <= 3:
            ax.plot(
                time_array,
                ne0,
                color="r",
                marker="o",
                label=r"$n_{e0} [10^{19}.m^{-3}]$",
            )
        else:
            ax.plot(time_array, ne0, color="r", label=r"$n_{e0} [10^{19}.m^{-3}]$")
        if len(time_array) != 1:
            ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(ip)*1.2)
        ax.legend(
            bbox_to_anchor=(1.0, 0.5),
            loc="center left",
            borderaxespad=0.0,
            frameon=False,
        )
        ax.set_ylim(0, 20)

    def plot_density_profile(self, ax, time_slice, psi_cordinate=False, update=True, logscale=False):
        """
        This function plots the electron density profile as a function of either the normalized toroidal flux
        coordinate or the poloidal magnetic flux coordinate.

        Args:
            ax: ax is a matplotlib axis object where the density profile plot will be drawn.
            time_slice: The time index refers to the specific time step or snapshot of data that is being plotted.
                It is used to retrieve the electron density and other relevant data at that particular time.
            psi_cordinate: A boolean parameter that determines whether the density profile should be plotted as a
                function of the poloidal flux coordinate (-psi) or the normalised toroidal flux coordinate (rho_tor).
                If psi_cordinate is True, the density profile will be plotted as a function of -psi. Defaults to False
            update: The `update` parameter is a boolean flag that determines whether the plot should be updated or
                created from scratch. If `update` is `True`, the function will create a new plot with the given data.
                If `update` is `False`, the function will update an existing plot with the new. Defaults to True
            logscale: log scale

        Returns:
            a tuple containing the matplotlib plot object for the electron density profile (ax_density_plot_dens)
            and the maximum electron density value (nmax).
        """
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)
        if rho_tor_norm is not None:
            radial_coordinate = rho_tor_norm
            xlabel = ""
            if update:
                xlabel = r"Normalised $\rho_{tor}$ [-]"
            if psi_cordinate:
                psi = self.core_profiles_compute.get_psi(time_slice)
                if psi is not None:
                    radial_coordinate = psi
                    if update:
                        xlabel = r"$-\psi$ [Wb]"

            ax.set_xlabel(xlabel)
            electron_density = self.ids.profiles_1d[time_slice].electrons.density
            nmax = max(electron_density) * 1.2
            ax_density_plot_dens = None
            if update:
                (ax_density_plot_dens,) = ax.plot(
                    radial_coordinate,
                    electron_density,
                    color="b",
                    label=r"$n_e [m^{-3}]$",
                )
                # ax_density.set_ylim(bottom=0,top=max(electron_density))
            else:
                ax.set_ylim(top=nmax)
                ax.set_data(radial_coordinate, electron_density)
            ax.legend(
                bbox_to_anchor=(1.0, 0.5),
                loc="center left",
                borderaxespad=0.0,
                frameon=False,
            )
            if logscale:
                ax.set_yscale("log")
            return ax_density_plot_dens, nmax

    def plot_ion_pressure_properties(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-6
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            logger.critical("----> Aborted.")
            return
        dict_ion_pressure_properties = self.core_profiles_compute.get_ion_pressure_properties(time_slice)
        maxima_ion = dict_ion_pressure_properties["maxima_ion"]
        pressure_ion_thermal = dict_ion_pressure_properties["pressure_ion_thermal"]
        pressure_ion_fast_parallel = dict_ion_pressure_properties["pressure_ion_fast_parallel"]
        pressure_ion_fast_perpendicular = dict_ion_pressure_properties["pressure_ion_fast_perpendicular"]

        ax.plot(rho_tor_norm, pressure_ion_thermal * FACTOR, label="Thermal ion")
        ax.plot(rho_tor_norm, pressure_ion_fast_parallel * FACTOR, label="Fast parallel ion")
        ax.plot(
            rho_tor_norm,
            pressure_ion_fast_perpendicular * FACTOR,
            label="Fast perpendicular ion",
        )
        ax.set_ylim(0, maxima_ion * FACTOR)
        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"P (MPa)", labelpad=0)
        ax.legend()
        ax.set_title("Ion Pressure Properties", loc="left")

    def show_info_on_plot(self, ax, info: str = "", location="right"):
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

    def plot_electron_pressure_properties(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-6
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            logger.critical("----> Aborted.")

        dict_electrons_pressure_properties = self.core_profiles_compute.get_electrons_pressure_properties(time_slice)
        maxima_electrons = dict_electrons_pressure_properties["maxima_electrons"]
        pressure_electron_total = dict_electrons_pressure_properties["pressure_electron_total"]
        pressure_electron_thermal = dict_electrons_pressure_properties["pressure_electron_thermal"]
        pressure_electron_fast_parallel = dict_electrons_pressure_properties["pressure_electron_fast_parallel"]
        pressure_electron_fast_perpendicular = dict_electrons_pressure_properties[
            "pressure_electron_fast_perpendicular"
        ]

        ax.plot(rho_tor_norm, pressure_electron_total * FACTOR, label="Total electron")
        ax.plot(rho_tor_norm, pressure_electron_thermal * FACTOR, label="Thermal electron")
        ax.plot(
            rho_tor_norm,
            pressure_electron_fast_parallel * FACTOR,
            label="Fast parallel electron",
        )
        ax.plot(
            rho_tor_norm,
            pressure_electron_fast_perpendicular * FACTOR,
            label="Fast perpendicular electron",
        )
        ax.set_ylim(0, maxima_electrons * FACTOR)

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"P (MPa)", labelpad=0)
        ax.legend()
        ax.set_title("Electrons Pressure Properties", loc="left")

    def plot_total_pressure_properties(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-6
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            return

        dict_pressure = self.core_profiles_compute.get_pressure(time_slice)
        maxima_total = dict_pressure["maxima_total"]
        pressure_total = dict_pressure["pressure_total"]
        pressure_thermal = dict_pressure["pressure_thermal"]
        pressure_parallel = dict_pressure["pressure_parallel"]
        pressure_perpendicular = dict_pressure["pressure_perpendicular"]

        if maxima_total == 0:
            logger.critical("No pressure profile found")
            return
        ax.plot(rho_tor_norm, pressure_total * FACTOR, label="Total")
        ax.plot(rho_tor_norm, pressure_thermal * FACTOR, label="Thermal")
        ax.plot(rho_tor_norm, pressure_parallel * FACTOR, label="Parallel")
        ax.plot(rho_tor_norm, pressure_perpendicular * FACTOR, label="Perpendicular")
        # ax.set_xlim(rhoTorNorm[0], rhoTorNorm[nrho - 1])
        ax.set_ylim(0, maxima_total * FACTOR)

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"P (MPa)", labelpad=0)
        ax.legend()
        ax.set_title("Total Pressure Properties", loc="left")

    def view_q_profile_and_magnetic_shear_profile(self, ax, time_slice, **kwargs):
        """
        The function `view_q_profile_and_magnetic_shear_profile` plots the q-profile and magnetic shear profile
        using the given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes
                on which the plot will be drawn.
        """
        profiles = self.core_profiles_compute.get_profiles(time_slice)

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

    def view_current_density_profiles(self, ax, time_slice, **kwargs):
        """
        The function `view_current_density_profiles` plots various current density profiles on a given axis.

        Args:
            ax: The parameter "ax" is an instance of the matplotlib Axes class. It represents the axes
                on which the plot will be drawn.
        """
        profiles = self.core_profiles_compute.get_profiles(time_slice)
        ax.plot(profiles["rhonorm"], profiles["j_total"] * 1.0e-3, label=r"$j_{TOT}$")
        ax.plot(profiles["rhonorm"], profiles["j_non_inductive"] * 1.0e-3, label=r"$j_{NI}$")
        ax.plot(profiles["rhonorm"], profiles["j_bootstrap"] * 1.0e-3, label=r"$j_{BOOT}$")
        ax.plot(profiles["rhonorm"], profiles["j_ohmic"] * 1.0e-3, label=r"$j_{OHM}$")

        ax.set_xlabel(r"$\rho/\rho_0$")
        ax.set_ylabel(r"$j\/[\mathrm{kA/m^2}]$")
        ax.set_xlim(0, 1)
        ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))

    def plot_efield_profile(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-3
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            return
        radial = self.ids.profiles_1d[time_slice].e_field.radial.value
        if len(radial) < 1:
            logger.critical(f"core_profiles.profiles_1d[{time_slice}].e_field.radial could not be read")
            radial = np.asarray([np.nan] * nrho)
        ax.plot(rho_tor_norm, radial * FACTOR, label="E-field")
        ax.set_xlim(rho_tor_norm[0], rho_tor_norm[nrho - 1])

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"E-field ($kV/m$)", labelpad=0)
        # set legend
        ax.legend()
        ax.set_title("Electric field profile", loc="left")

    def plot_toroidal_velocity_profile(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-3
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            return

        nions = len(self.ids.profiles_1d[time_slice].ion)
        species = self.core_profiles_compute.get_species(time_slice)
        if species:
            for ion_index in range(nions):
                toroidal = self.ids.profiles_1d[time_slice].ion[ion_index].velocity.toroidal.value
                if len(toroidal) < 1:
                    logger.critical(
                        f"core_profiles.profiles_1d[{time_slice}].ion[{ion_index}].velocity.toroidal could not be read"
                    )
                    toroidal = np.asarray([np.nan] * nrho)
                ax.plot(
                    rho_tor_norm,
                    toroidal * FACTOR,
                    label=species[ion_index],
                )

        ax.set_xlim(rho_tor_norm[0], rho_tor_norm[nrho - 1])

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"$v_{tor}$ ($km/s$)", labelpad=0)
        # TODO update
        # ax2.yaxis.tick_right()
        # ax2.yaxis.set_label_position("right")
        # set legend
        # legx_pos = 1.35
        # legy_pos = 1.05
        ax.legend()
        ax.set_title("Toroidal velocity profile", loc="left")

    def plot_poloidal_velocity_profile(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-3
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty",
            )
            return

        nions = len(self.ids.profiles_1d[time_slice].ion)
        species = self.core_profiles_compute.get_species(time_slice)
        if species:
            for ion_index in range(nions):
                poloidal = self.ids.profiles_1d[time_slice].ion[ion_index].velocity.poloidal.value
                if len(poloidal) < 1:
                    logger.critical(
                        f"core_profiles.profiles_1d[{time_slice}].ion[{ion_index}].velocity.poloidal could not be read"
                    )
                    poloidal = np.asarray([np.nan] * nrho)
                ax.plot(
                    rho_tor_norm,
                    poloidal * FACTOR,
                    label=species[ion_index],
                )

        ax.set_xlim(rho_tor_norm[0], rho_tor_norm[nrho - 1])

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"$v_{pol}$ ($km/s$)", labelpad=0)

        # set legend
        ax.legend()
        ax.set_title("Poloidal velocity profile", loc="left")

    def plot_diamagnetic_velocity_profile(self, ax, time_slice, **kwargs):
        FACTOR = 1.0e-3
        rho_tor_norm = self.core_profiles_compute.get_rho_tor_norm(time_slice)  # Rho profile (mandatory)
        nrho = len(rho_tor_norm)
        if nrho == 0:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor/"
                f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm) is empty"
            )
            return

        nions = len(self.ids.profiles_1d[time_slice].ion)
        species = self.core_profiles_compute.get_species(time_slice)
        if species:
            for ion_index in range(nions):
                diamagnetic = self.ids.profiles_1d[time_slice].ion[ion_index].velocity.diamagnetic.value

                if len(diamagnetic) < 1:
                    logger.critical(
                        f"core_profiles.profiles_1d[{time_slice}].ion[{ion_index}].velocity.diamagnetic"
                        "could not be read"
                    )
                    diamagnetic = np.asarray([np.nan] * nrho)
                ax.plot(
                    rho_tor_norm,
                    diamagnetic * FACTOR,
                    label=species[ion_index],
                )

        ax.set_xlim(rho_tor_norm[0], rho_tor_norm[nrho - 1])
        # ax4.yaxis.tick_right()
        # ax4.yaxis.set_label_position("right")

        ax.set_xlabel(r"$\rho/\rho_0$", labelpad=1)
        ax.set_ylabel(r"$v_{dia}$ ($km/s$)", labelpad=0)

        # set legend
        ax.legend()
        ax.set_title("Diamagnetic velocity profile", loc="left")
