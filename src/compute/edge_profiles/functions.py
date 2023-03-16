import numpy as np
import database_tools.init_mendeleiev as mend
import sys
import functools

import logging

logger = logging.getLogger("module." + __name__)

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
        try:
            ids_object.ggd[slice_index]

        except:
            logger.critical("!  edge_profiles IDS:slice not found")
            return 0

        edgeProfilesCompute = EdgeProfilesCompute(ids_object, slice_index)

        if edgeProfilesCompute.get_volume(slice_index) is None:
            return -1

        data = {}
        nspec_over_ntot = edgeProfilesCompute.get_nspec_over_ntot()
        nspec_over_ne = edgeProfilesCompute.get_nspec_over_ne()
        nspec_over_nmaj = edgeProfilesCompute.get_nspec_over_nmaj()
        species = edgeProfilesCompute.get_species()
        labels = edgeProfilesCompute.get_labels()
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
            species_data["states"] = states_data[str(species_index)]
            species_data["label"] = labels[species_index]

            data[str(species_index)] = species_data

        return data

    def get_labels(self, slice_index=0):  # done
        nspecies = len(self.ids_object.ggd[slice_index].ion)
        labels = []
        for ispecies in range(nspecies):
            labels.append(self.ids_object.ggd[slice_index].ion[ispecies].label)

        logger.debug("Species identification :" + str(labels))
        return labels

    @functools.lru_cache(maxsize=128)
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
            a[ispecies] = (
                self.ids_object.ggd[slice_index].ion[ispecies].element[element_index].a
            )

        logger.debug("Mass of atom : " + str(a))
        return a

    @functools.lru_cache(maxsize=128)
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
        logger.debug("Nuclear charge each species : " + str(z))
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

        volume = self.get_volume(slice_index)
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

                for xd in (
                    self.ids_object.ggd[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .z_average
                ):
                    if xd.grid_subset_index == 5:
                        state_data["z_average"] = xd.values[0]

                for xd in (
                    self.ids_object.ggd[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .density
                ):
                    if xd.grid_subset_index == 5:
                        states_density[state_index] = sum(
                            np.array(volume) * np.array(xd.values)
                        )
                        break
                state_data["states_density"] = states_density
                state_data["n_ni"] = (
                    100 * states_density[state_index] / species_density[species_index]
                )
                species_data[str(state_index)] = state_data
            states_data[str(species_index)] = species_data
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
        electron_density = self.get_density(slice_index)
        # electron_density = self.ids_object.ggd[slice_index].electrons.density[0].values
        logger.info("Total no. electrons (ne): " + str(sum(volume * electron_density)))
        return sum(volume * electron_density)

    # Discussed with Xavier read 31 and 32 from dd
    @functools.lru_cache(maxsize=128)
    def get_volume(self, slice_index=0):  # Done
        index = 4
        elements = self.ids_object.grid_ggd[slice_index].grid_subset[index].element
        grid_subset_name = (
            self.ids_object.grid_ggd[slice_index].grid_subset[index].identifier.name
        )
        logger.info(grid_subset_name)
        # check if grid_subset[4] identifier name is cells, if not, find out 'cells' index
        index_counter = 0
        if grid_subset_name.lower() != "cells":
            logger.warning(
                "!  edge_profiles IDS:cells not found in grid subset at 4th index, Checking index of cells"
            )
            for subset in self.ids_object.grid_ggd[slice_index].grid_subset:
                if subset.identifier.name.lower() == "cells":
                    elements = (
                        self.ids_object.grid_ggd[slice_index]
                        .grid_subset[index_counter]
                        .element
                    )
                    grid_subset_name = (
                        self.ids_object.grid_ggd[slice_index]
                        .grid_subset[index_counter]
                        .identifier.name
                    )
                    index = index_counter
                    logger.warning(
                        "!  edge_profiles IDS:cells found in grid subset at "
                        + str(index_counter)
                        + " index"
                    )
                    break
                index_counter = index_counter + 1
        num_vertices = len(elements)
        if num_vertices == 0:
            logger.critical(
                "!  edge_profiles IDS:No element found in grid subset : " + str()
            )
            return None
        volumes = [0] * num_vertices

        for index, element in enumerate(elements):
            for obj in element.object:
                # Get mapping information from element like, space, dimension and index which we need to look in space object
                space_index = obj.space - 1
                dimension_index = obj.dimension - 1
                object_index = obj.index - 1

                # Get geometry_content.index to check what is stored in the geometry array
                geometry_content_index = (
                    self.ids_object.grid_ggd[slice_index]
                    .space[space_index]
                    .objects_per_dimension[dimension_index]
                    .geometry_content.index
                )
                # if geometry_content => face_indices_volume or face_indices_volume_connection it contains the volume
                if geometry_content_index == 31 or geometry_content_index == 32:
                    # Get the object which is mapped from grid_subset to space
                    obj_dim = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[dimension_index]
                        .object[object_index]
                    )
                    # The third element contains the volume, read the same
                    volumes[index] = obj_dim.geometry[2]
        if np.any(volumes) == False:
            logger.warning(
                "!  edge_profiles IDS:volume is not available in cells (face_indices_volume).. Calculating manually from nodes "
            )
            # Get volume from nodes if volumes are still empty
            for index, element in enumerate(elements):
                for obj in element.object:
                    # Get mapping information from element like, space, dimension and index which we need to look in space object
                    space_index = obj.space - 1
                    dimension_index = obj.dimension - 1
                    object_index = obj.index - 1

                    # Get all nodes of the cell object
                    nodes = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[dimension_index]
                        .object[object_index]
                        .nodes
                    )
                    # Decrement by 1 to compensate zero based indexing
                    nodes = nodes - 1
                    # Get R and Z values from nodes deom object_per_dimesnion 0
                    R1, Z1 = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[0]]
                        .geometry
                    )
                    R2, Z2 = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[1]]
                        .geometry
                    )

                    R3, Z3 = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[2]]
                        .geometry
                    )
                    R4, Z4 = (
                        self.ids_object.grid_ggd[slice_index]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[3]]
                        .geometry
                    )
                    area = 0.5 * (
                        (R1 * Z2 + R2 * Z3 + R3 * Z4 + R4 * Z1)
                        - (R2 * Z1 + R3 * Z2 + R4 * Z3 + R1 * Z4)
                    )
                    baryR = (
                        1.0
                        / (6.0 * area)
                        * (
                            (R1 + R2) * (R1 * Z2 - R2 * Z1)
                            + (R2 + R3) * (R2 * Z3 - R3 * Z2)
                            + (R3 + R4) * (R3 * Z4 - R4 * Z3)
                            + (R4 + R1) * (R4 * Z1 - R1 * Z4)
                        )
                    )

                    volumes[index] = 2.0 * np.pi * baryR * area

        if np.any(volumes) == False:
            logger.critical("!   edge_profiles IDS: volumes are empty")
            return None
        logger.info("Total volume:" + str(np.sum(volumes)))
        return volumes

    def get_density(self, slice_index=0):  # done
        density_ion = None
        for xd in self.ids_object.ggd[slice_index].electrons.density:
            if xd.grid_subset_index == 5:
                density_ion = xd.values
                break
        logger.debug("Electrons density array:" + str(density_ion))
        logger.info("Total Electrons density:" + str(sum(density_ion)))
        return density_ion

    @functools.lru_cache(maxsize=128)
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
        volume = self.get_volume(slice_index)
        ntot = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            for xd in self.ids_object.ggd[slice_index].ion[ispecies].density:
                if xd.grid_subset_index == 5:
                    species_density_list[ispecies] = sum(
                        np.array(volume) * np.array(xd.values)
                    )
                    break

            if len(self.ids_object.ggd[slice_index].ion[ispecies].density) == 0:
                logger.warn(
                    "!   edge_profiles IDS: species density not found for "
                    + self.ids_object.ggd[slice_index].ion[ispecies].label
                    + ", Getting density from state."
                )
                density = None
                for counter, state in enumerate(
                    self.ids_object.ggd[slice_index].ion[ispecies].state
                ):
                    for xd in state.density:
                        if xd.grid_subset_index == 5:
                            if counter == 0:
                                density = np.array([0] * len(xd.values))
                                density = np.add(density, np.array(xd.values))
                            else:
                                density = np.add(density, np.array(xd.values))
                            break
                species_density_list[ispecies] = sum(np.array(volume) * density)
            ntot = ntot + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
        logger.debug("Species density : " + str(species_density_list))
        logger.debug("Sum of Species Density (ntot) : " + str(ntot))
        logger.debug("Index of Maximum Density Species : " + str(max_density_index))
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

        a = list(map(int, self.get_a()))
        z = list(map(int, self.get_z()))
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
