from ...compute.core_profiles.functions import CoreProfilesCompute
from ...view.common.functions import Console


class CoreProfilesView(Console):
    def __init__(self):
        pass

    @staticmethod
    def view_plasma_composition_with_species_concentration(
        ids_object, slice_index=0, print_data=False
    ):
        """
        Nice display of plasma composition with species concentrations
        """
        composition_data = (
            CoreProfilesCompute.get_plasma_composition_with_species_concentration(
                ids_object, slice_index
            )
        )

        coreProfilesView = CoreProfilesView()
        coreProfilesView._print_plasma_composition(composition_data)
        coreProfilesView._print_specis_concentration(composition_data)

        if print_data is True:
            import json

            print(json.dumps(composition_data, sort_keys=True, indent=4))

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
                    + " " * (self.tabsize - len(species_data["species"]))
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

        for species_key, species_data in composition_data.items():
            states = species_data["states"]
            nstates = len(states)
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
            for state_key, state_data in states.items():
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
                istate += 1
