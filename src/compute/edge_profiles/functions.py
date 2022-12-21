import numpy as np
import database_tools.init_mendeleiev as mend
import json

# TODO Create base class for Edge and Core as methods are same but way of retriving is different Many common methods
# TODO Use strategy after that
class EdgeProfilesCompute:
    def __init__(self, ids_object, slice_index=0):
        super().__init__()
        self.ids_object = ids_object
        self.slice_index = slice_index

    @staticmethod
    def get_plasma_composition_with_species_concentration(
        ids_object, slice_index=0
    ) -> dict:
        """
        Function retrives composition and species concentration in below format
            Spcies_label
                a
                nspec_over_ne
                nspec_over_nmaj
                nspec_over_ntot
                species [mendeleiev_table]
                states
                    label
                    n_ni
                    states_density [list]
                    z_average
        Folllowing is the example
        {
            "D": {
                "a": 2,
                "z": 1
                "nspec_over_ne": 0.5023622549575154,
                "nspec_over_nmaj": 1.0,
                "nspec_over_ntot": 0.5037968786242728,
                "species": mendeleiev_table,
                "states": {
                    "0": {
                        "label": "",
                        "n_ni": 100.0,
                        "states_density": [
                            8.368879805142247e+23
                        ],
                        "z_average": -9e+40
                    }
                },
            },
        }
        Args:
            ids_object ([ids_object]): [filled ids object]
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [dict]: [species wise data in dictionary format]
        """
        edgeProfilesCompute = EdgeProfilesCompute(ids_object, slice_index)

        data = {}

        nspec_over_ntot = edgeProfilesCompute.get_nspec_over_ntot()
        nspec_over_ne = edgeProfilesCompute.get_nspec_over_ne()
        nspec_over_nmaj = edgeProfilesCompute.get_nspec_over_nmaj()
        species = edgeProfilesCompute.get_species()
        edgeProfilesCompute.combine_species_when_appear_twice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj
        )
        a = edgeProfilesCompute.get_a()
        z = edgeProfilesCompute.get_z()
        states_data = edgeProfilesCompute.get_states_data()
        for species_index in range(len(species)):
            species_data = {}
            species_data["nspec_over_ntot"] = nspec_over_ntot[species_index]
            species_data["nspec_over_ne"] = nspec_over_ne[species_index]
            species_data["nspec_over_nmaj"] = nspec_over_nmaj[species_index]
            species_data["a"] = a[species_index]
            species_data["z"] = z[species_index]
            species_data["species"] = species[species_index]
            species_data["states"] = states_data[species[species_index]]

            data[species[species_index]] = species_data

        return data

    def get_a(self, slice_index=0, element_index=0) -> list:  # done
        """
        Get series wise value of a of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            element_index (int, optional): [element on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise values of [a] of all species ]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        a = [0] * nspecies
        for ispecies in range(nspecies):
            a[ispecies] = int(
                self.ids_object.ggd[slice_index].ion[ispecies].element[element_index].a
            )
        return a

    def get_z(self, slice_index=0, element_index=0) -> list:  # done
        """
        Get series wise value of z of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            element_index (int, optional): [element on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise values of [z] of all species ]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        z = [0] * nspecies
        for ispecies in range(nspecies):
            z[ispecies] = int(
                self.ids_object.ggd[slice_index]
                .ion[ispecies]
                .element[element_index]
                .z_n
            )
        return z

    # TODO Removed this method as it is not used anywhere
    # def get_zeff(self, slice_index=0, element_index=0):
    #     return self.ids_object.profiles_1d[slice_index].zeff[element_index]

    def get_states(self, slice_index=0):  # Done
        """
        Get series wise data of states of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise data of states of all species ]
        """
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        states = []
        for species_index in range(nspecies):
            states.append(self.ids_object.ggd[slice_index].ion[species_index].state)
        return states

    def get_states_data(self, slice_index=0) -> dict:  # done
        """
        Get data of states in dictionary format

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [dict]: [data of states in dictionary format]
        """

        states_data = {}

        # TODO return np.array itself get_volume
        volume = self.get_volume()
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        species_density, _, _ = self.get_species_density()
        for species_index in range(nspecies):
            species_data = {}
            nstates = len(self.ids_object.ggd[slice_index].ion[species_index].state)
            states_density = [0] * nstates
            for state_index in range(nstates):
                state_data = {}
                state_data["label"] = (
                    self.ids_object.ggd[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .label
                )
                # TODO Why [0].values
                state_data["z_average"] = np.mean(
                    self.ids_object.ggd[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .z_average[0]
                    .values
                )

                try:
                    states_density[state_index] = sum(
                        (
                            self.ids_object.ggd[slice_index]
                            .ion[species_index]
                            .state[state_index]
                            .density[0]
                            .values
                            * volume
                        )
                    )
                except:
                    try:
                        states_density[state_index] = sum(
                            self.ids_object.ggd[slice_index]
                            .ion[species_index]
                            .state[state_index]
                            .density_thermal[0]
                            .values
                            * volume
                        )
                    except:
                        print("!  Error with density data")
                state_data["states_density"] = states_density
                state_data["n_ni"] = (
                    100 * states_density[state_index] / species_density[species_index]
                )
                species_data[str(state_index)] = state_data
            label = self.ids_object.ggd[slice_index].ion[species_index].label
            states_data[label] = species_data
        return states_data

    def get_ne(self, slice_index=0) -> float:  # done
        """
        Sum of multiplication of volume and elcetrons density

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [float]: [Sum of multiplication of volume and elcetrons density ]
        """
        volume = self.get_volume(slice_index)
        electron_density = self.ids_object.ggd[slice_index].electrons.density[0].values
        return sum(volume * electron_density)

    def get_volume(self, slice_index=0):  # Done
        num_vertices = len(
            self.ids_object.grid_ggd[slice_index]
            .space[0]
            .objects_per_dimension[0]
            .object
        )
        volumes = [0] * num_vertices

        for i in range(num_vertices):
            index = (
                self.ids_object.grid_ggd[slice_index]
                .grid_subset[0]
                .element[i]
                .object[0]
                .index
            )
            volumes[i] = (
                self.ids_object.grid_ggd[slice_index]
                .space[0]
                .objects_per_dimension[2]
                .object[index]
                .measure
            )
            if volumes[i] < 0:
                volume_error = "!   objects exist but self.ids_object.grid_ggd[0].space[0].objects_per_dimension[0].object volumes are empty, replaced by 1"
                volumes[i] = 1

        return volumes

    def get_density(self, slice_index=0):  # done
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        volumes = self.get_volumes()
        density_ion = None
        for species_index in range(nspecies):
            # First try to read ion.density
            try:
                density_ion = (
                    self.ids_object.ggd[slice_index]
                    .ion[species_index]
                    .density[0]
                    .values
                )
            except:
                # If not, try in ion.thermal_density
                try:
                    density_ion = (
                        self.ids_object.ggd[slice_index]
                        .ion[species_index]
                        .density_thermal[0]
                        .values
                    )
                except:
                    # If not, try to read all ion states density and sum
                    try:
                        nstates = len(
                            self.ids_object.ggd[slice_index].ion[species_index].state
                        )
                        density_ion = [0] * len(volumes)
                        for istate in range(nstates):
                            density_ion = (
                                density_ion
                                + self.ids_object.ggd[slice_index]
                                .ion[species_index]
                                .state[istate]
                                .density[0]
                                .values
                            )
                    except:
                        density_ion = [0] * len(volumes)
                        # print('!   No density data for ion', species_edge[species_index])
        return density_ion

    def get_single_species_density(self, slice_index=0):  # done
        """
        Sum of multiplication of volume and species density

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            species_index (int, optional): [species from which we need to get the data]. Defaults to 0.

        Returns:
            [float]: [Sum of multiplication of volume and elcetrons density ]
        """
        volume = self.get_volume(slice_index)
        density = self.get_density()
        # TODO To return  np .array from functions itself
        return sum(np.array(volume) * np.array(density))

    def get_species_density(self, slice_index=0) -> tuple:  # done
        """
        Returns species_density_list, sum_density, max_density_index of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [float]: [species_density_list list of all species density]
            [float]: [sum_density Sum of densities]
            [float]: [max_density_index index at which it has maximum density]
        """
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        ntot = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            species_density_list[ispecies] = self.get_single_species_density(
                slice_index=0, species_index=ispecies
            )
            ntot = ntot + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
        return species_density_list, ntot, max_density_index

    def get_nspec_over_ntot(self):  # done
        """
        Get series wise values of nspec_over_ntot

        Returns:
            [list]: [retruns list of series wise species property nspec_over_ntot]
        """

        species_density_list, ntot, _ = self.get_species_density()
        return species_density_list / ntot

    def get_nspec_over_ne(self):  # done
        """
        Get series wise values of nspec_over_ne

        Returns:
            [list]: [retruns list of series wise species property nspec_over_ne]
        """
        species_density_list, _, _ = self.get_species_density()
        ne = self.get_ne()
        return species_density_list / ne

    def get_nspec_over_nmaj(self) -> list:  # done
        """
        Get series wise values of nspec_over_nmaj

        Returns:
            [list]: [retruns list of series wise species property nspec_over_nmaj]
        """
        (
            species_density_list,
            _,
            max_density_index,
        ) = self.get_species_density()
        return species_density_list / species_density_list[max_density_index]

    def get_species(self, slice_index=0) -> list:  # done
        """
        Creates mendeleiev table and put values of a anz z and return the series wise list of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            list: [Returns mendeleiev table and put values of a anz z and return the series wise list of all species]
        """
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids_object.ggd[slice_index].ion)

        a = self.get_a()
        z = self.get_z()
        species = []
        for ispecies in range(nspecies):
            species.append(table_mendeleiev[z[ispecies]][a[ispecies]].element)
        return species

    def combine_species_when_appear_twice(
        self, species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj, slice_index=0
    ):  # done
        """
        This is helper function which checks if there are dupliacte entries of species and combine the species.

        This is in place change of arrays

        Args:
            species ([list]): [description]
            nspec_over_ntot ([list]): [description]
            nspec_over_ne ([list]): [description]
            nspec_over_nmaj ([list]): [description]
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
        """
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        for ispecies in range(nspecies):
            for jspecies in range(nspecies):
                if (species[jspecies] == species[ispecies]) & (jspecies != ispecies):
                    nspec_over_ntot[ispecies] = (
                        nspec_over_ntot[ispecies] + nspec_over_ntot[jspecies]
                    )
                    nspec_over_ntot[jspecies] = 0
                    nspec_over_ne[ispecies] = (
                        nspec_over_ne[ispecies] + nspec_over_ne[jspecies]
                    )
                    nspec_over_ne[jspecies] = 0
                    nspec_over_nmaj[ispecies] = (
                        nspec_over_nmaj[ispecies] + nspec_over_nmaj[jspecies]
                    )
                    nspec_over_nmaj[jspecies] = 0
