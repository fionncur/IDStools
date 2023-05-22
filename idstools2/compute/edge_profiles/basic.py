""" 
This module provides compute functions and classes for equilibrium ids data

`more about edge_profiles ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/edge_profiles.html>`_.

"""

import functools
import itertools
import logging
import numpy as np

import database_tools.init_mendeleiev as mend

logger = logging.getLogger("module")

class EdgeProfilesCompute:
    def __init__(self, ids):
        self.ids = ids

    @staticmethod
    def getPlasmaCompositionWithSpeciesConcentration(
        ids, timeSlice=0
    ) -> dict:
        """
        Function retrives composition and species concentration in below format
            - Spcies_label
                - a
                - nspec_over_ne
                - nspec_over_nmaj
                - nspec_over_ntot
                - species [mendeleiev_table]
                - states
                    - label
                    - n_ni
                    - states_density [list]
                    - z_average
        
        Args:
            ids ([ids_object]): [filled ids object]
            timeSlice (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [dict]: [species wise data in dictionary format]
            
        Example:
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                result = EdgeProfilesCompute.getPlasmaCompositionWithSpeciesConcentration(idsObj, 0)
                    
                {'0': 
                    {'a': 2.0,
                    'label': 'D',
                    'nspec_over_ne': 0.0,
                    'nspec_over_nmaj': 0.0,
                    'nspec_over_ntot': 0.0,
                    'species': 'D',
                    'states': 
                        {'0': 
                            {'label': ' D+1',
                            'n_ni': 100.0,
                            'states_density': [1.6577031350573213e+22],
                            'z_average': 1.0}},
                            'z': 1},
                '1': 
                    {'a': 4.0,
                    'label': 'He',
                    'nspec_over_ne': 0.007831354424836625,
                    'nspec_over_nmaj': 0.008250985371197173,
                    'nspec_over_ntot': 0.008146485662619047,
                    'species': 'He4',
                    'states': 
                        {'0': 
                            {'label': ' He+1',
                            'n_ni': 0.9279275264034698,
                            'states_density': [1.2691899775336492e+18,
                            1.3550765319392264e+20],
                            'z_average': 1.0},
                        '1': 
                            {'label': ' He+2',
                            'n_ni': 99.07207247359639,
                            'states_density': [1.2691899775336492e+18, 1.3550765319392264e+20],
                            'z_average': 2.0}},
                            'z': 2},
        """
        try:
            ids.ggd[timeSlice]

        except Exception:
            logger.critical("edge_profiles IDS:slice not found")
            return 0

        edgeProfilesCompute = EdgeProfilesCompute(ids)

        if edgeProfilesCompute.getVolume(timeSlice) is None:
            return -1

        data = {}
        nspec_over_ntot = edgeProfilesCompute.getNspecOverNtot()
        nspec_over_ne = edgeProfilesCompute.getNspecOverNe()
        nspec_over_nmaj = edgeProfilesCompute.getNspecOverNmaj()
        species = edgeProfilesCompute.getSpecies()
        labels = edgeProfilesCompute.getLabels()
        edgeProfilesCompute.combineSpeciesWhenAppearTwice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj
        )
        a = edgeProfilesCompute.get_a()
        z = edgeProfilesCompute.get_z()
        states_data = edgeProfilesCompute.getStatesData()
        for species_index in range(len(species)):
            species_data = {
                "nspec_over_ntot": nspec_over_ntot[species_index],
                "nspec_over_ne": nspec_over_ne[species_index],
                "nspec_over_nmaj": nspec_over_nmaj[species_index],
                "a": a[species_index],
                "z": z[species_index],
                "species": species[species_index],
                "states": states_data[str(species_index)],
                "label": labels[species_index],
            }
            data[str(species_index)] = species_data

        return data

    def getLabels(self, timeSlice=0):  
        """
        This function returns a list of labels for all species in a given time slice.
        
        Args:
            timeSlice: an optional integer parameter that specifies the time slice on which the function should operate. The default value is 0
        
        Returns:
            a list of labels for all species in a given time slice.
            
        Example:
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getLabels(timeSlice=0)

                ['D', 'He', 'Ne', 'Be', ' D2+']
        """
        
        nspecies = len(self.ids.ggd[timeSlice].ion)
        labels = [
            self.ids.ggd[timeSlice].ion[ispecies].label
            for ispecies in range(nspecies)
        ]
        logger.debug(f"Species identification :{labels}")
        return labels

    @functools.lru_cache(maxsize=128)
    def get_a(self, timeSlice=0, elementIndex=0) -> list:  
        """
        This function returns a list of atomic masses for a given slice and element index.

        Args:
            timeSlice (int, optional): The index of the slice in the `ggd` list that contains the ion information.Defaults to 0
            elementIndex (int, optional): Element index, It is used to access the 'a' attribute of the element object. Defaults to 0

        Returns:
            a list of atomic masses for each species in the given slice index and element index. 
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.get_a(timeSlice=0)
            
                [2.0, 4.0, 20.0, 9.0, 2.0]
        """
        nspecies = len(self.ids.ggd[timeSlice].ion)
        a = [0] * nspecies
        for ispecies in range(nspecies):
            a[ispecies] = (
                self.ids.ggd[timeSlice].ion[ispecies].element[elementIndex].a
            )

        logger.debug(f"Mass of atom : {str(a)}")
        return a

    @functools.lru_cache(maxsize=128)
    def get_z(self, timeSlice=0, elementIndex=0) -> list:   
        """
        This function returns a list of nuclear charges for each species in a given slice and element
        index.
        
        Args:
            timeSlice (int, optional): time slice on which functions should operate on. Defaults to 0.
            elementIndex (int, optional): element of the atom or molecule on which functions should operate on. Defaults to 0.
        
        Returns:
            a list of nuclear charges for each species in the given timeSlice and elementIndex.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.get_z(timeSlice=0)
            
                [1, 2, 10, 4, 1]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids.ggd[timeSlice].ion)
        z = [0] * nspecies
        for ispecies in range(nspecies):
            z[ispecies] = int(
                self.ids.ggd[timeSlice]
                .ion[ispecies]
                .element[elementIndex]
                .z_n
            )
        logger.debug(f"Nuclear charge each species : {z}")
        return z

    def getStates(self, timeSlice=0):
        """
        This function returns quantities related to the different states of the species (ionisation, energy, excitation, ...) for each species
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            a list of states (ionisation, energy, excitation, etc.) in  the input data of each species .
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getStates(timeSlice=0)

                print(result[0]) # state object from species
                
                # class 'imas_3_38_1_ual_4_11_4.edge_profiles.ggd_ion_state__structArray'
        """
        nspecies = len(self.ids.ggd[timeSlice].ion)
        return [
            self.ids.ggd[timeSlice].ion[iSpecies].state
            for iSpecies in range(nspecies)
        ]

    def getStatesData(self, timeSlice=0) -> dict:   
        """
        This function returns a dictionary containing data on the states and densities of different species in a plasma simulation.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            a dictionary containing information about the states of different species in a plasma, including their labels, z-averages, densities, and relative densities.
            
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getStatesData(timeSlice=0)    
            
                {'0': 
                {'0': 
                {'label': ' D+1',
                'n_ni': 100.0,
                'states_density': [1.6577031350573213e+22],
                'z_average': 1.0}},
                '1': 
                {'0': {'label': ' He+1',
                'n_ni': 0.9279275264034698,
                'states_density': [1.2691899775336492e+18, 1.3550765319392264e+20],
                'z_average': 1.0},
                '1': 
                {'label': ' He+2',
                'n_ni': 99.07207247359639,
                'states_density': [1.2691899775336492e+18, 1.3550765319392264e+20],
                'z_average': 2.0}},
        """

        states_data = {}

        volume = self.getVolume(timeSlice)
        nspecies = len(self.ids.ggd[timeSlice].ion)
        species_density, _, _ = self.getSpeciesDensity()
        for species_index in range(nspecies):
            species_data = {}
            nstates = len(self.ids.ggd[timeSlice].ion[species_index].state)
            states_density = [0] * nstates
            for state_index in range(nstates):
                state_data = {
                    "label": self.ids.ggd[timeSlice]
                    .ion[species_index]
                    .state[state_index]
                    .label
                }
                for xd in (
                    self.ids.ggd[timeSlice]
                    .ion[species_index]
                    .state[state_index]
                    .z_average
                ):
                    if xd.grid_subset_index == 5:
                        state_data["z_average"] = xd.values[0]

                for xd in (
                    self.ids.ggd[timeSlice]
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

    def get_ne(self, timeSlice=0) -> float:   
        """
        This function calculates the total number of electrons (ne) based on the volume and electron density of a given slice.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            the total number of electrons (ne) in the given slice of the object, calculated by multiplying the volume of the slice with its electron density and summing the results.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.get_ne(timeSlice=0)      
            
                1.7465285792413856e+22
        """
        volume = self.getVolume(timeSlice)
        electron_density = self.getDensity(timeSlice)
        logger.info(f"Total no. electrons (ne): {str(sum(volume * electron_density))}")
        return sum(volume * electron_density)

    @functools.lru_cache(maxsize=128)
    def getVolume(self, timeSlice=0)->list: 
        """
        This function calculates the volume of a grid subset using either pre-calculated volume data or by manually calculating it from the nodes.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            a list of volumes for each element in the grid subset. If the volumes are not available in the cells, it calculates the volumes manually from the nodes. If the volumes are still empty, it returns None. Finally, it returns the volumes list.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getVolume(timeSlice=0) 
                
                [0.00037247887179986,
                0.00036873285033229,
                0.00036505732877168,
                0.00035287806726545,
                0.00034083126399982,
                0.00032428140427918,
                0.00030192063059504,
                0.00027702026849475,
                0.0002505748085483,
                0.00021528820409221]
        """
        IDENTIFIER_CELLS_INDEX = 4 # cells identifier 
        elements = self.ids.grid_ggd[timeSlice].grid_subset[IDENTIFIER_CELLS_INDEX].element
        grid_subset_name = (
            self.ids.grid_ggd[timeSlice].grid_subset[IDENTIFIER_CELLS_INDEX].identifier.name
        )
        logger.info(grid_subset_name)
        # check if grid_subset[4] identifier name is cells, if not, find out 'cells' index
        index_counter = 0
        if grid_subset_name.lower() != "cells":
            logger.warning(
                "edge_profiles IDS:cells not found in grid subset at 4th index, Checking index of cells in the grid subset"
            )
            for subset in self.ids.grid_ggd[timeSlice].grid_subset:
                if subset.identifier.name.lower() == "cells":
                    elements = (
                        self.ids.grid_ggd[timeSlice]
                        .grid_subset[index_counter]
                        .element
                    )
                    grid_subset_name = (
                        self.ids.grid_ggd[timeSlice]
                        .grid_subset[index_counter]
                        .identifier.name
                    )
                    IDENTIFIER_CELLS_INDEX = index_counter
                    logger.warning(f"edge_profiles IDS:cells found in grid subset at {IDENTIFIER_CELLS_INDEX} index")
                    break
                index_counter = index_counter + 1
        num_vertices = len(elements)
        if num_vertices == 0:
            logger.critical("edge_profiles IDS:No element found in grid subset")
            return None
        volumes = [0] * num_vertices

        for ielement, element in enumerate(elements):
            for obj in element.object:
                # Get mapping information from element like, space, dimension and index which we need to look in space object
                space_index = obj.space - 1
                dimension_index = obj.dimension - 1
                object_index = obj.index - 1

                # Get geometry_content.index to check what is stored in the geometry array
                geometry_content_index = (
                    self.ids.grid_ggd[timeSlice]
                    .space[space_index]
                    .objects_per_dimension[dimension_index]
                    .geometry_content.index
                )
                # if geometry_content => face_indices_volume or face_indices_volume_connection it contains the volume
                if geometry_content_index in [31, 32]:
                    # Get the object which is mapped from grid_subset to space
                    obj_dim = (
                        self.ids.grid_ggd[timeSlice]
                        .space[space_index]
                        .objects_per_dimension[dimension_index]
                        .object[object_index]
                    )
                    # The third element contains the volume, read the same
                    volumes[ielement] = obj_dim.geometry[2]
        if np.any(volumes) == False:
            logger.warning(
                "edge_profiles IDS:volume is not available in cells (face_indices_volume).. Calculating manually from nodes "
            )
            # Get volume from nodes if volumes are still empty
            for ielement, element in enumerate(elements):
                for obj in element.object:
                    # Get mapping information from element like, space, dimension and index which we need to look in space object
                    space_index = obj.space - 1
                    dimension_index = obj.dimension - 1
                    object_index = obj.index - 1

                    # Get all nodes of the cell object
                    nodes = (
                        self.ids.grid_ggd[timeSlice]
                        .space[space_index]
                        .objects_per_dimension[dimension_index]
                        .object[object_index]
                        .nodes
                    )
                    # Decrement by 1 to compensate zero based indexing
                    nodes = nodes - 1
                    # Get R and Z values from nodes deom object_per_dimesnion 0
                    R1, Z1 = (
                        self.ids.grid_ggd[timeSlice]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[0]]
                        .geometry
                    )
                    R2, Z2 = (
                        self.ids.grid_ggd[timeSlice]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[1]]
                        .geometry
                    )

                    R3, Z3 = (
                        self.ids.grid_ggd[timeSlice]
                        .space[space_index]
                        .objects_per_dimension[0]
                        .object[nodes[2]]
                        .geometry
                    )
                    R4, Z4 = (
                        self.ids.grid_ggd[timeSlice]
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

                    volumes[ielement] = 2.0 * np.pi * baryR * area

        if np.any(volumes) == False:
            logger.critical("edge_profiles IDS: volumes are empty")
            return None
        logger.info(f"Total volume:{np.sum(volumes)}")
        return volumes

    def getDensity(self, timeSlice=0): 
        """
        This function retrieves the electron density array for a given slice index and returns it.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            the electron density array for a specific slice index, and also logging the array and the total electron density.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getDensity(timeSlice=0) 
                
                array([1.83014037e+19, 2.86305333e+19, 4.50302324e+19, 6.99266610e+19,
                1.04025196e+20, 1.56969187e+20, 2.32851365e+20, 3.45402170e+20,
                4.94164863e+20, 7.07373803e+20])
        """
        densityIon = next(
            (
                xd.values
                for xd in self.ids.ggd[timeSlice].electrons.density
                if xd.grid_subset_index == 5
            ),
            None,
        )
        logger.debug(f"Electrons density array:{densityIon}")
        logger.info(f"Total Electrons density:{sum(densityIon)}")
        return densityIon

    @functools.lru_cache(maxsize=128)
    def getSpeciesDensity(self, timeSlice=0) -> tuple:  
        """
        This function calculates the density of different species in a given slice and returns a tuple containing the species density list, the total density, and the index of the species with the maximum density.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            a tuple containing three values: a list of species density, the total density of all species, and the index of the species with the maximum density.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getSpeciesDensity(timeSlice=0) 
                
                ([1.6577031350573213e+22,
                1.3677684317145648e+20,
                6.227201649981566e+19,
                1.3510799045753078e+19,
                8.356155820974862e+16],
                1.6789674570848447e+22,
                0)
        """
        nspecies = len(self.ids.ggd[timeSlice].ion)
        volume = self.getVolume(timeSlice)
        ntot = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            for xd in self.ids.ggd[timeSlice].ion[ispecies].density:
                if xd.grid_subset_index == 5:
                    species_density_list[ispecies] = sum(
                        np.array(volume) * np.array(xd.values)
                    )
                    break

            if len(self.ids.ggd[timeSlice].ion[ispecies].density) == 0:
                logger.warn(
                    "edge_profiles IDS: species density not found for "
                    + self.ids.ggd[timeSlice].ion[ispecies].label
                    + ", Getting density from state."
                )
                density = None
                for counter, state in enumerate(
                    self.ids.ggd[timeSlice].ion[ispecies].state
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
        logger.debug(f"Species density : {species_density_list}")
        logger.debug(f"Sum of Species Density (ntot) : {ntot}")
        logger.debug(f"Index of Maximum Density Species : {max_density_index}" )
        return species_density_list, ntot, max_density_index

    def getNspecOverNtot(self, timeSlice=0): 
        """
        This function calculates the ratio of the number of species to the total number of particles in a plasma.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
            
        Returns:
            The function `getNspecOverNtot` is returning the ratio of the list of species densities to the  total density (`ntot`).
            
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getNspecOverNtot(timeSlice=0) 
                
                array([9.87334881e-01, 8.14648566e-03, 3.70894720e-03, 8.04708810e-04, 4.97696116e-06])

        """
        species_density_list, ntot, _ = self.getSpeciesDensity(timeSlice)
        return species_density_list / ntot

    def getNspecOverNe(self, timeSlice=0):  
        """
        This function calculates the ratio of species density to electron density.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            the ratio of the species density list to the electron density (ne).
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getNspecOverNe(timeSlice=0) 
                
                array([9.49141717e-01, 7.83135442e-03, 3.56547366e-03, 7.73580187e-04, 4.78443692e-06])
        """
        species_density_list, _, _ = self.getSpeciesDensity(timeSlice)
        ne = self.get_ne()
        return species_density_list / ne

    def getNspecOverNmaj(self, timeSlice=0) -> list:  
        """
        This function returns a list of the ratio of each species density to the maximum species density.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
            
        Returns:
            a list of values obtained by dividing each element of the list `species_density_list` by the maximum value in that list. This list represents the ratio of the density of each species to the density of the most abundant species.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getNspecOverNmaj() 
                
                array([1.00000000e+00, 8.25098537e-03, 3.75652402e-03, 8.15031278e-04,5.04080353e-06])
        """
        (
            species_density_list,
            _,
            max_density_index,
        ) = self.getSpeciesDensity(timeSlice)
        return species_density_list / species_density_list[max_density_index]

    def getSpecies(self, timeSlice=0) -> list:
        """
        This function creates a Mendeleiev table and returns a list of species based on the values of a,
        z, and the table.
        
        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        
        Returns:
            a list of species based on the values of a, z, and the Mendeleev table.
            
        Example:                 
            .. code-block:: python
            
                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',123276,1,'public')
                connection.open()
                idsObj = connection.get('edge_profiles')
                computeObj = EdgeProfilesCompute(idsObj)
                result = computeObj.getSpecies() 
            
                ['D', 'He4', 'Ne', 'Be', 'D']
        """
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids.ggd[timeSlice].ion)

        a = list(map(int, self.get_a()))
        z = list(map(int, self.get_z()))
        return [
            table_mendeleiev[z[ispecies]][a[ispecies]].element
            for ispecies in range(nspecies)
        ]

    def combineSpeciesWhenAppearTwice(
        self, species, nspecOverNtot, nspecOverNe, nspecOverNmaj, timeSlice=0
    ):    
        """
        This is helper function which checks if there are duplicate entries of species and combine the species. This is in place change of arrays

        Args:
            species (list): result from getSpecies()
            nspecOverNtot (list): result from getNspecOverNtot()
            nspecOverNe (list): result from getNspecOverNe()
            nspecOverNmaj (list): result from getNspecOverNmaj()
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.
        """
        nspecies = len(self.ids.ggd[timeSlice].ion)
        for ispecies, jspecies in itertools.product(range(nspecies), range(nspecies)):
            if (species[jspecies] == species[ispecies]) & (jspecies != ispecies):
                nspecOverNtot[ispecies] = (
                    nspecOverNtot[ispecies] + nspecOverNtot[jspecies]
                )
                nspecOverNtot[jspecies] = 0
                nspecOverNe[ispecies] = (
                    nspecOverNe[ispecies] + nspecOverNe[jspecies]
                )
                nspecOverNe[jspecies] = 0
                nspecOverNmaj[ispecies] = (
                    nspecOverNmaj[ispecies] + nspecOverNmaj[jspecies]
                )
                nspecOverNmaj[jspecies] = 0
