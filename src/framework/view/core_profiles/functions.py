from ...compute.core_profiles.functions import CoreProfilesCompute


class CoreProfilesView:
    def __init__(self, ids_object, slice_index=0):
        self.ids_object = ids_object
        self.slice_index = slice_index

    def view_plasma_composition_with_species_concentration(self):
        """
        Nice display of plasma composition with species concentrations
        """
        composition_data = (
            CoreProfilesCompute.get_plasma_composition_with_species_concentration(
                self.ids_object, self.slice_index
            )
        )
        self._print_plasma_composition(composition_data)
        self._print_specis_concentration(composition_data)

    def _print_plasma_composition(self, composition_data):
        nspecies = composition_data["nspecies"]
        nspec_over_ntot = composition_data["nspec_over_ntot"]
        nspec_over_nmaj = composition_data["nspec_over_nmaj"]
        nspec_over_ne = composition_data["nspec_over_ne"]
        species = composition_data["species"]
        a = composition_data["a"]
        z = composition_data["z"]

        disp_species = "   species:      "
        disp_a = "   a:            "
        disp_z = "   z:            "
        disp_nspec_over_ntot = "   n_over_ntot:  "
        disp_nspec_over_ne = "   n_over_ne:    "
        disp_nspec_over_nmaj = "   n_over_n_maj: "
        main_species = ""

        for ispecies in range(nspecies):
            if nspec_over_ntot[ispecies] > 0.45:
                if len(main_species) == 0:
                    main_species = main_species + species[ispecies]
                else:
                    main_species = main_species + "-" + species[ispecies]
            if nspec_over_ne[ispecies] > 0.0:
                tabsize = 10
                disp_species = (
                    disp_species
                    + species[ispecies]
                    + " " * (tabsize - len(species[ispecies]))
                )
                disp_a = (
                    disp_a
                    + format("%.1f" % a[ispecies])
                    + " " * (tabsize - len(format("%.1f" % a[ispecies])))
                )
                disp_z = (
                    disp_z
                    + format("%.1f" % z[ispecies])
                    + " " * (tabsize - len(format("%.1f" % z[ispecies])))
                )
                if nspec_over_ntot[ispecies] < 1.0e-2:
                    disp_nspec_over_ntot = (
                        disp_nspec_over_ntot
                        + format("%.2e" % nspec_over_ntot[ispecies])
                        + " "
                        * (tabsize - len(format("%.2e" % nspec_over_ntot[ispecies])))
                    )
                else:
                    disp_nspec_over_ntot = (
                        disp_nspec_over_ntot
                        + format("%.3f" % nspec_over_ntot[ispecies])
                        + " "
                        * (tabsize - len(format("%.3f" % nspec_over_ntot[ispecies])))
                    )
                if nspec_over_ne[ispecies] < 1.0e-2:
                    disp_nspec_over_ne = (
                        disp_nspec_over_ne
                        + format("%.2e" % nspec_over_ne[ispecies])
                        + " "
                        * (tabsize - len(format("%.2e" % nspec_over_ne[ispecies])))
                    )
                else:
                    disp_nspec_over_ne = (
                        disp_nspec_over_ne
                        + format("%.3f" % nspec_over_ne[ispecies])
                        + " "
                        * (tabsize - len(format("%.3f" % nspec_over_ne[ispecies])))
                    )
                if nspec_over_nmaj[ispecies] < 1.0e-2:
                    disp_nspec_over_nmaj = (
                        disp_nspec_over_nmaj
                        + format("%.2e" % nspec_over_nmaj[ispecies])
                        + " "
                        * (tabsize - len(format("%.2e" % nspec_over_nmaj[ispecies])))
                    )
                else:
                    disp_nspec_over_nmaj = (
                        disp_nspec_over_nmaj
                        + format("%.3f" % nspec_over_nmaj[ispecies])
                        + " "
                        * (tabsize - len(format("%.3f" % nspec_over_nmaj[ispecies])))
                    )
        print("   ------------")
        print("core_profiles")
        print("   ------------")
        print(disp_species)
        print(disp_a)
        print(disp_z)
        print(disp_nspec_over_ntot)
        print(disp_nspec_over_ne)
        print(disp_nspec_over_nmaj)
        print("   ------------")

    def _print_specis_concentration(self, composition_data):
        TAB = " " * 16
        LINE = "-" * 8
        states_data = composition_data["states_data"]
        for species_key, species_value in states_data.items():
            nstates = len(species_value)
            if nstates > 1:
                comm = "s"
            else:
                comm = ""
            print(
                species_key,
                " has ",
                nstates,
                " state" + comm,
            )
            istate = 0
            for state_key, state_value in species_value.items():
                print(
                    TAB,
                    "state ",
                    str(istate + 1),
                    (" " * (5 - len(str(istate + 1)))),
                    state_value["label"],
                    (" " * (7 - len(str(state_value["label"])))),
                    "z =",
                    state_value["z_average"],
                    (" " * (7 - len(str(state_value["z_average"])))),
                    "   n/ni, % :",
                    format("%.6f" % (state_value["n_ni"])),
                )
                istate += 1
