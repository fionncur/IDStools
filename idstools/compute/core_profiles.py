""" 
This module provides compute functions and classes for core_profiles ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import contextlib
from typing import Union
import numpy as np
import idstools.init_mendeleiev as mend
import logging
import functools

import itertools

logger = logging.getLogger("module")


class CoreProfilesCompute:
    def __init__(self, ids, volume=None):
        self.ids = ids
        self.volume = volume

    @staticmethod
    def getPlasmaCompositionWithSpeciesConcentration(
        ids, timeSlice=0, volume=None
    ) -> dict:
        """
        Function retrives composition and species concentration in below format
        """
        try:
            ids.profiles_1d[timeSlice]

        except Exception as e:
            return 0

        coreProfileCompute = CoreProfilesCompute(ids, volume=volume)

        if coreProfileCompute.volume is None:
            volume = coreProfileCompute.getVolume(timeSlice)
            if volume is None:
                return -1
            else:
                coreProfileCompute.volume = volume
        data = {}

        nspec_over_ntot = coreProfileCompute.getNspecOverNtot()
        nspec_over_ne = coreProfileCompute.getNspecOverNe()
        nspec_over_nmaj = coreProfileCompute.getNspecOverNmaj()
        species = coreProfileCompute.getSpecies()
        labels = coreProfileCompute.getLabels()
        coreProfileCompute.combine_species_when_appear_twice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj
        )
        a = coreProfileCompute.get_a()
        z = coreProfileCompute.get_z()
        states_data = coreProfileCompute.getStatesData()
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

    @functools.lru_cache(maxsize=128)
    def getElectronDensityNe0(self):
        """
        This function returns a list of electron densities at the first position for each time step in a given object.

        Returns:
            The function `get_ne0` returns a list of electron densities at the first spatial point (index 0) for all time steps in the simulation. The electron density is in units of 1e-19 m^-3.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',105033,1,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getElectronDensityNe0(timeSlice=0)

                [5.106128949975287]
        """
        ntime = len(self.ids.time)

        return [
            self.ids.profiles_1d[itime].electrons.density[0] * 1.0e-19
            for itime in range(ntime)
        ]

    @functools.lru_cache(maxsize=128)
    def get_a(self, timeSlice=0, element_index=0) -> list:
        """
        This function returns a list of atomic masses for a given slice and element index.

        Args:
            timeSlice (int, optional): The index of the slice in the `ggd` list that contains the ion information.Defaults to 0
            element_index (int, optional): Element index, It is used to access the 'a' attribute of the element object. Defaults to 0

        Returns:
            a list of atomic masses for each species in the given slice index and element index.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',105033,1,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_a(timeSlice=0)

                [2.0, 3.0, 4.0, 9.0, 183.84, 40.0, 20.0]
        """
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        a = [0] * nspecies
        for ispecies in range(nspecies):
            a[ispecies] = (
                self.ids.profiles_1d[timeSlice].ion[ispecies].element[element_index].a
            )
        logger.debug(f"Mass of atom : {a}")
        return a

    @functools.lru_cache(maxsize=128)
    def get_z(self, timeSlice: int = 0, elementIndex: int = 0) -> list:
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
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',105033,1,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_z(timeSlice=0)

                [1, 1, 2, 4, 74, 18, 10]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        z = [0] * nspecies
        for ispecies in range(nspecies):
            z[ispecies] = int(
                self.ids.profiles_1d[timeSlice].ion[ispecies].element[elementIndex].z_n
            )
        logger.debug(f"Nuclear charge each species : {z}")
        return z

    def getStates(self, timeSlice: int = 0) -> list:
        """
        This function returns quantities related to the different states of the species (ionisation, energy, excitation, ...) for each species

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of states (ionisation, energy, excitation, etc.) in  the input data of each species .

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',105033,1,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getStates(timeSlice=0)

                print(result[0]) # state object from species

                # class 'imas_3_38_1_ual_4_11_4.core_profiles.profiles_1d_ion_state__structArray'
        """
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        return [
            self.ids.profiles_1d[timeSlice].ion[species_index].state
            for species_index in range(nspecies)
        ]

    def getStateDensity(
        self, timeSlice: int = 0, speciesIndex: int = 0, stateIndex: int = 0
    ) -> np.ndarray:
        """
        This function returns the density of a specified state of a specified species at a specified time slice, or the thermal density if the former is not available.

        Args:
            timeSlice (int): an integer representing the index of the time slice for which the density is being requested. Defaults to 0
            speciesIndex (int): The index of the ion species for which the density is being retrieved. Defaults to 0
            stateIndex (int): The index of the state for which the density is being retrieved. Defaults to 0

        Returns:
            a numpy array containing the density of a specified state of a specified species at a specified time slice. If the density is not available, it returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getStateDensity(timeSlice=0, speciesIndex=0, stateIndex=0)

                array([4.16759116e+19, 4.17266130e+19, 4.17275806e+19, 4.17086410e+19,
                4.16751781e+19, 4.16983762e+19, 4.17344996e+19, 4.17944658e+19,
        """
        with contextlib.suppress(Exception):
            density = (
                self.ids.profiles_1d[timeSlice]
                .ion[speciesIndex]
                .state[stateIndex]
                .density
            )
            if len(density) != 0:
                return density
        with contextlib.suppress(Exception):
            density = (
                self.ids.profiles_1d[timeSlice]
                .ion[speciesIndex]
                .state[stateIndex]
                .density_thermal
            )
            if len(density) != 0:
                return density
        return None

    def getStatesData(self, timeSlice: int = 0) -> dict:
        """
        This function returns a dictionary containing data on the states and densities of different species in a plasma simulation.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a dictionary containing information about the states of different species in a plasma, including their labels, z-averages, densities, and relative densities.


        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getStatesData(timeSlice=0)


                {'0': {'0': {'density_available': True,
                'label': '',
                'n_ni': 100.0,
                'states_density': [6.50016400579169e+23],
                'z_average': -9e+40}},
                '1': {'0': {'density_available': True,
                'label': '',
                'n_ni': 0.023001604469815865,
                'states_density': [1.906627956029117e+19, 8.287201892847867e+22],
                'z_average': -9e+40},
        """

        volume = self.getVolume(timeSlice)
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        species_density, _, _ = self.getSpeciesDensity()
        states_data = {}
        for species_index in range(nspecies):
            logger.debug(f"Species index :{species_index}")
            logger.debug(f"Species density :{species_density[species_index]}")
            species_data = {}
            nstates = len(self.ids.profiles_1d[timeSlice].ion[species_index].state)
            logger.debug(f"Species states count :{nstates}")
            states_density = [0] * nstates
            for state_index in range(nstates):
                state_data = {
                    "label": self.ids.profiles_1d[timeSlice]
                    .ion[species_index]
                    .state[state_index]
                    .label,
                    "z_average": np.mean(
                        self.ids.profiles_1d[timeSlice]
                        .ion[species_index]
                        .state[state_index]
                        .z_average
                    ),
                }

                density = self.getStateDensity(timeSlice, species_index, state_index)
                state_data["density_available"] = False
                if density is None:
                    logger.critical(
                        f"core_profile IDS: Density data for species {self.ids.profiles_1d[timeSlice].ion[species_index].label} and state {str(state_index)} is empty "
                    )
                elif len(density) != 0:
                    # if all density values in the array are 1.0 or 0.0 then do not calculate because it can be false values
                    if np.all(density == 1.0) or np.all(density == 0.0):
                        logger.critical(
                            f"core_profile IDS: Density data for species {self.ids.profiles_1d[timeSlice].ion[species_index].label} and state {str(state_index)} all are ones or zeros "
                        )
                    else:
                        logger.debug(f"Density array :{density}")
                        states_density[state_index] = sum(density * volume)
                        state_data["density_available"] = True
                else:
                    logger.critical(
                        f"core_profile IDS: Density data for species {self.ids.profiles_1d[timeSlice].ion[species_index].label}",
                        f" and state {state_index} is empty ",
                    )
                # TODO Couldn't retrive state desnity should we calculate n/ni?
                # In that case density is always 0 and no meaning of n/ni
                # We can also get weired errors
                #  idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: invalid value encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                # idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: divide by zero encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                state_data["states_density"] = states_density
                logger.debug(
                    f"State density at index {state_index} : State density : {states_density[state_index]}"
                    + "\t Species density :"
                    + str(species_density[species_index])
                )
                # if species density is 0.0 then do not calculate n/ni
                if species_density[species_index] != 0.0:
                    state_data["n_ni"] = (
                        100
                        * states_density[state_index]
                        / species_density[species_index]
                    )
                else:
                    state_data["n_ni"] = 0.0
                species_data[str(state_index)] = state_data

            # label = self.ids_object.profiles_1d[timeSlice].ion[species_index].label
            states_data[str(species_index)] = species_data
        return states_data

    def get_ne(self, timeSlice: int = 0) -> float:
        """
        This function calculates the total number of electrons (ne) based on the volume and electron density of a given slice.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the total number of electrons (ne) in the given slice of the object, calculated by multiplying the volume of the slice with its electron density and summing the results.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_ne(timeSlice=0)

                8.778296205101714e+23
        """
        volume = self.getVolume(timeSlice)

        electron_density = self.ids.profiles_1d[timeSlice].electrons.density
        logger.info(f"Total no. electrons (ne): {str(sum(volume * electron_density))}")
        return sum(volume * electron_density)

    @functools.lru_cache(maxsize=128)
    def getVolume(self, timeSlice: int = 0) -> np.ndarray:
        """
        This function returns the volume of a grid at a given time slice.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the volume of the grid for a given time slice. If the volume is empty, it returns None

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getVolume(timeSlice=0)

                array([4.39932160e-02, 2.19952424e-01, 5.71837023e-01, 1.09958863e+00,
                1.80311391e+00, 2.68234060e+00, 3.73724537e+00, 4.96778828e+00,
        """
        volume = self.ids.profiles_1d[timeSlice].grid.volume
        if len(volume) == 0:
            volume = None
            logger.critical("core_profile IDS: Grid volume is empty")
        logger.info(f"Total volume:{np.sum(volume)}")
        return volume

    @functools.lru_cache(maxsize=128)
    def getSpeciesDensity(self, timeSlice: int = 0) -> tuple:
        """
        This function calculates the density of different species in a given slice and returns a tuple containing the species density list, the total density, and the index of the species with the maximum density.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a tuple containing three values: a list of species density, the total density of all species, and the index of the species with the maximum density.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getSpeciesDensity(timeSlice=0)

                ([6.50016400579169e+23, 8.289108520803897e+22, 6.202712465391594e+21],7.391101982525995e+23, 0)
        """
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        sum_density = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            volume = self.getVolume(timeSlice)
            density = self.ids.profiles_1d[timeSlice].ion[ispecies].density
            species_density_list[ispecies] = sum(volume * density)

            sum_density = sum_density + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
        logger.debug(f"Species density:{str(species_density_list)}")
        return species_density_list, sum_density, max_density_index

    def getNspecOverNtot(self, timeSlice: int = 0):
        """
        This function calculates the ratio of the number of species to the total number of particles in a plasma.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            The function `getNspecOverNtot` is returning the ratio of the list of species densities to the  total density (`ntot`).

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getNspecOverNtot(timeSlice=0)

                array([0.87945803, 0.11214983, 0.00839213])
        """
        species_density_list, sum_density, _ = self.getSpeciesDensity(timeSlice)
        return species_density_list / sum_density

    def getNspecOverNe(self, timeSlice: int = 0):
        """
        This function calculates the ratio of species density to electron density.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the ratio of the species density list to the electron density (ne).

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getNspecOverNe(timeSlice=0)

                array([0.74048128, 0.0944273 , 0.00706596])
        """
        species_density_list, _, _ = self.getSpeciesDensity(timeSlice)
        ne = self.get_ne()
        return species_density_list / ne

    def getNspecOverNmaj(self, timeSlice: int = 0) -> list:
        """
        This function returns a list of the ratio of each species density to the maximum species density.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of values obtained by dividing each element of the list `species_density_list` by the maximum value in that list. This list represents the ratio of the density of each species to the density of the most abundant species.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getNspecOverNmaj(timeSlice=0)

                array([1.        , 0.12752153, 0.00954239])
        """
        (
            species_density_list,
            _,
            max_density_index,
        ) = self.getSpeciesDensity(timeSlice)
        return species_density_list / species_density_list[max_density_index]

    def getSpecies(self, timeSlice: int = 0) -> list:
        """
        This function creates a Mendeleiev table and returns a list of species based on the values of a, z, and the table.

        Args:
            timeSlice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of species based on the values of a, z, and the Mendeleev table.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getSpecies(timeSlice=0)

                ['H', 'He4', 'Ne']
        """
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)

        a = list(map(int, self.get_a()))
        z = list(map(int, self.get_z()))
        return [
            table_mendeleiev[z[ispecies]][a[ispecies]].element
            for ispecies in range(nspecies)
        ]

    def getLabels(self, timeSlice: int = 0) -> list:
        """
        This function returns a list of labels for all species in a given time slice.

        Args:
            timeSlice: an optional integer parameter that specifies the time slice on which the function should operate. The default value is 0

        Returns:
            a list of labels for all species in a given time slice.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getLabels(timeSlice=0)

                ['H', 'He', 'Ne']
        """
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        labels = [
            self.ids.profiles_1d[timeSlice].ion[ispecies].label
            for ispecies in range(nspecies)
        ]
        logger.debug(f"Species identification :{labels}")
        return labels

    def combine_species_when_appear_twice(
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
        nspecies = len(self.ids.profiles_1d[timeSlice].ion)
        for ispecies, jspecies in itertools.product(range(nspecies), range(nspecies)):
            if (species[jspecies] == species[ispecies]) & (jspecies != ispecies):
                nspecOverNtot[ispecies] = (
                    nspecOverNtot[ispecies] + nspecOverNtot[jspecies]
                )
                nspecOverNtot[jspecies] = 0
                nspecOverNe[ispecies] = nspecOverNe[ispecies] + nspecOverNe[jspecies]
                nspecOverNe[jspecies] = 0
                nspecOverNmaj[ispecies] = (
                    nspecOverNmaj[ispecies] + nspecOverNmaj[jspecies]
                )
                nspecOverNmaj[jspecies] = 0

    def getRhoTorNorm(self, timeSlice: int = 0) -> np.ndarray:
        """
        This function returns a list of normalized toroidal rho values from a given time slice of a profiles_1d object.

        Args:
            timeSlice (int): time index. Defaults to 0

        Returns:
            a list of normalized toroidal flux coordinates (rho_tor_norm) for a given time slice of the IDS object. If rho_tor_norm is not available, it tries to return a list of toroidal flux coordinates (rho_tor) instead. If neither is available, it returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getRhoTorNorm(timeSlice=0)

                [0.005025125628140704,
                0.015075376884422112,
                0.035175879396984924,
                0.045226130653266326,
                0.05527638190954774]
        """
        try:
            if len(self.ids.profiles_1d[timeSlice].grid.rho_tor_norm) > 0:
                return self.ids.profiles_1d[timeSlice].grid.rho_tor_norm
            elif len(self.ids.profiles_1d[timeSlice].grid.rho_tor) > 0:
                return (
                    self.ids.profiles_1d[timeSlice].grid.rho_tor
                    / self.ids.profiles_1d[timeSlice].grid.rho_tor[-1]
                )
        except IndexError:
            logger.error(
                f"core_profiles.profiles_1d[{timeSlice}].grid.rho_tor_norm or rho_tor is not available"
            )
        return None

    def getPSI(self, timeSlice: int = 0) -> list:
        """
        This function returns the poloidal magnetic flux (psi) at a given time slice.

        Args:
            timeSlice (int): time index

        Returns:
            the poloidal magnetic flux (psi) as a list of floats for a given time slice. If the length of the poloidal magnetic flux is greater than 0, then the function returns the negative of the poloidal magnetic flux. If the length of the poloidal magnetic flux is 0, then the function returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',104010,2,'public')
                connection.open()
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.getPSI(timeSlice=0)

                array([-4.95660880e+01, -4.95537345e+01, -4.95275298e+01, -4.94833135e+01,
                -4.94209348e+01, -4.93461904e+01, -4.92595767e+01, -4.91573223e+01,

        """
        psi = None
        if len(self.ids.profiles_1d[timeSlice].grid.psi) > 0:
            psi = -self.ids.profiles_1d[timeSlice].grid.psi
        return psi

    def getIonPressureProperties(self):
        """
        The function `getIonPressureProperties` calculates and returns the total thermal pressure, fast parallel pressure, and fast perpendicular pressure of ions in a given set of profiles.

        Returns:
            a dictionary with the following keys and values:

            .. code-block:: python

                {
                    "maximaIon": maximaIon,
                    "pressureIonThermal": pressureIonThermal,
                    "pressureIonFastParallel": pressureIonFastParallel,
                    "pressureIonFastPerpendicular": pressureIonFastPerpendicular,
                }
        """
        nrho = len(self.getRhoTorNorm())
        pressureIonThermal = 0.0
        pressureIonFastParallel = 0.0
        pressureIonFastPerpendicular = 0.0
        for ion in self.ids.profiles_1d[0].ion:
            if len(ion.pressure_thermal) == 0:
                logger.warn("Empty profiles_1d[0].ion.pressure_thermal")
            if len(ion.pressure_fast_parallel) == 0:
                logger.warn("Empty profiles_1d[0].ion.pressure_fast_parallel")
            if len(ion.pressure_fast_perpendicular) == 0:
                logger.warn("Empty profiles_1d[0].ion.pressure_fast_perpendicular")
            pressureIonThermal = pressureIonThermal + ion.pressure_thermal
            pressureIonFastParallel = (
                pressureIonFastParallel + np.asarray([np.nan] * nrho)
                if len(ion.pressure_fast_parallel) == 0
                else ion.pressure_fast_parallel
            )
            pressureIonFastPerpendicular = (
                pressureIonFastPerpendicular + np.asarray([np.nan] * nrho)
                if len(ion.pressure_fast_perpendicular) == 0
                else ion.pressure_fast_perpendicular
            )

        pressureIonThermal = (
            np.asarray([np.nan] * nrho)
            if len(pressureIonThermal) == 0
            else pressureIonThermal
        )
        pressureIonFastParallel = (
            np.asarray([np.nan] * nrho)
            if len(pressureIonFastParallel) == 0
            else pressureIonFastParallel
        )
        pressureIonFastPerpendicular = (
            np.asarray([np.nan] * nrho)
            if len(pressureIonFastPerpendicular) == 0
            else pressureIonFastPerpendicular
        )

        maximaIon = max(
            np.nan_to_num(max(pressureIonThermal[: nrho - 1])),
            np.nan_to_num(max(pressureIonFastParallel[: nrho - 1])),
            np.nan_to_num(max(pressureIonFastPerpendicular[: nrho - 1])),
        )
        maximaIon = maximaIon * 1.1
        return {
            "maximaIon": maximaIon,
            "pressureIonThermal": pressureIonThermal,
            "pressureIonFastParallel": pressureIonFastParallel,
            "pressureIonFastPerpendicular": pressureIonFastPerpendicular,
        }

    def getElectronsPressureProperties(self):
        """
        The `getElectronsPressureProperties` function returns a dictionary containing various pressure properties of electrons, including the maximum pressure and individual pressure components.

        Returns:
            The function `getElectronsPressureProperties` returns a dictionary with the following key-value pairs:
            maximaElectrons, pressureElectronTotal, pressureElectronThermal,pressureElectronFastParallel, pressureElectronFastPerpendicular

        """
        nrho = len(self.getRhoTorNorm())
        pressureElectronTotal = self.ids.profiles_1d[0].electrons.pressure
        pressureElectronThermal = self.ids.profiles_1d[0].electrons.pressure_thermal
        pressureElectronFastParallel = self.ids.profiles_1d[
            0
        ].electrons.pressure_fast_parallel
        pressureElectronFastPerpendicular = self.ids.profiles_1d[
            0
        ].electrons.pressure_fast_perpendicular
        if len(pressureElectronTotal) == 0:
            logger.warn("Empty profiles_1d[0].electrons.pressure")
        if len(pressureElectronThermal) == 0:
            logger.warn("Empty profiles_1d[0].electrons.pressure_thermal")
        if len(pressureElectronFastParallel) == 0:
            logger.warn("Empty profiles_1d[0].electrons.pressure_fast_parallel")
        if len(pressureElectronFastPerpendicular) == 0:
            logger.warn("Empty profiles_1d[0].electrons.pressure_fast_perpendicular")
        pressureElectronTotal = (
            np.asarray([np.nan] * nrho)
            if len(pressureElectronTotal) == 0
            else pressureElectronTotal
        )
        pressureElectronThermal = (
            np.asarray([np.nan] * nrho)
            if len(pressureElectronThermal) == 0
            else pressureElectronThermal
        )
        pressureElectronFastParallel = (
            np.asarray([np.nan] * nrho)
            if len(pressureElectronFastParallel) == 0
            else pressureElectronFastParallel
        )
        pressureElectronFastPerpendicular = (
            np.asarray([np.nan] * nrho)
            if len(pressureElectronFastPerpendicular) == 0
            else pressureElectronFastPerpendicular
        )

        maximaElectrons = max(
            np.nan_to_num(max(pressureElectronTotal[: nrho - 1])),
            np.nan_to_num(max(pressureElectronThermal[: nrho - 1])),
            np.nan_to_num(max(pressureElectronFastParallel[: nrho - 1])),
            np.nan_to_num(max(pressureElectronFastPerpendicular[: nrho - 1])),
        )
        maximaElectrons = maximaElectrons * 1.1
        return {
            "maximaElectrons": maximaElectrons,
            "pressureElectronTotal": pressureElectronTotal,
            "pressureElectronThermal": pressureElectronThermal,
            "pressureElectronFastParallel": pressureElectronFastParallel,
            "pressureElectronFastPerpendicular": pressureElectronFastPerpendicular,
        }

    def getPressure(self):
        """
        The function `getPressure` returns a dictionary containing the thermal pressure, parallel pressure, and perpendicular pressure.

        Returns:
            a dictionary with three key-value pairs. The keys are "pressureThermal", "pressureParallel",and "pressurePerpendicular", and the values are the corresponding variables pressureThermal, pressureParallel, and pressurePerpendicular.

        """
        nrho = len(self.getRhoTorNorm())
        pressureThermal = self.ids.profiles_1d[0].pressure_thermal
        pressureParallel = self.ids.profiles_1d[0].pressure_parallel
        pressurePerpendicular = self.ids.profiles_1d[0].pressure_perpendicular
        if len(pressureThermal) == 0:
            logger.warn("Empty profiles_1d[0].pressure_thermal")
        if len(pressureParallel) == 0:
            logger.warn("Empty profiles_1d[0].pressure_fast_parallel")
        if len(pressurePerpendicular) == 0:
            logger.warn("Empty profiles_1d[0].pressure_fast_perpendicular")
        pressureThermal = (
            np.asarray([np.nan] * nrho)
            if len(pressureThermal) == 0
            else pressureThermal
        )
        pressureParallel = (
            np.asarray([np.nan] * nrho)
            if len(pressureParallel) == 0
            else pressureParallel
        )
        pressurePerpendicular = (
            np.asarray([np.nan] * nrho)
            if len(pressurePerpendicular) == 0
            else pressurePerpendicular
        )

        dictElectronsPressureProperties = self.getElectronsPressureProperties()
        pressureElectronTotal = dictElectronsPressureProperties["pressureElectronTotal"]

        pressureIonTotal = self.getPressureIonTotal()
        pressureTotal = pressureElectronTotal
        if pressureIonTotal is not None:
            pressureTotal += pressureIonTotal

        # Minima and maxima calculations for plots
        maximaTotal = max(
            np.nan_to_num(max(pressureTotal[: nrho - 1])),
            np.nan_to_num(max(pressureThermal[: nrho - 1])),
            np.nan_to_num(max(pressureParallel[: nrho - 1])),
            np.nan_to_num(max(pressurePerpendicular[: nrho - 1])),
        )

        maximaTotal = maximaTotal * 1.1

        return {
            "maximaTotal": maximaTotal,
            "pressureTotal": pressureTotal,
            "pressureThermal": pressureThermal,
            "pressureParallel": pressureParallel,
            "pressurePerpendicular": pressurePerpendicular,
        }

    def getPressureIonTotal(self) -> Union[float, None]:
        """
        The function `getPressureIonTotal` returns the total ion pressure from a given set of profiles, or None if the pressure values cannot be read.

        Returns:
            the value of the variable `pressureIonTotal`, which is either a float value or `None`.
        """
        pressureIonTotal = None
        if len(self.ids.profiles_1d[0].pressure_ion_total) > 1:
            pressureIonTotal = self.ids.profiles_1d[0].pressure_ion_total
        else:
            logger.critical(
                "core_profiles.profiles_1d[0].pressure_ion_total could not be read",
            )
            if len(self.ids.profiles_1d[0].ion[0].pressure) > 1:
                pressureIonTotal = 0.0
                for ion in self.ids.profiles_1d[0].ion:
                    pressureIonTotal = pressureIonTotal + ion.pressure
            else:
                logger.critical(
                    "core_profiles.profiles_1d[0].ion[0].pressure could not be read",
                )
        return pressureIonTotal

    def getProfiles(self, sliceIndex=0):
        rhoTorNorm = self.getRhoTorNorm(timeSlice=0)
        if rhoTorNorm is None:
            logger.critical(
                "core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty"
            )
            logger.critical("----> Aborted.")
            return None

        nrho = len(rhoTorNorm)

        # J_bootstrap profile
        if len(self.ids.profiles_1d[sliceIndex].j_bootstrap) < 1:
            logger.critical(
                "core_profiles.profiles_1d["
                + str(sliceIndex)
                + "].j_bootstrap could not be read"
            )
            self.ids.profiles_1d[sliceIndex].j_bootstrap = np.asarray([np.nan] * nrho)

        # J_non_inductive profile
        if len(self.ids.profiles_1d[sliceIndex].j_non_inductive) < 1:
            logger.critical(
                "core_profiles.profiles_1d["
                + str(sliceIndex)
                + "].j_non_inductive could not be read"
            )
            self.ids.profiles_1d[sliceIndex].j_non_inductive = np.asarray(
                [np.nan] * nrho
            )

        # J_ohmic profile
        if len(self.ids.profiles_1d[0].j_ohmic) < 1:
            logger.critical(
                "core_profiles.profiles_1d["
                + str(sliceIndex)
                + "].j_ohmic could not be read"
            )
            self.ids.profiles_1d[0].j_ohmic = np.asarray([np.nan] * nrho)

        # J_total profile
        if len(self.ids.profiles_1d[0].j_total) < 1:
            logger.critical(
                "core_profiles.profiles_1d["
                + str(sliceIndex)
                + "].j_total could not be read"
            )
            self.ids.profiles_1d[0].j_total = np.asarray([np.nan] * nrho)

        # q-profile
        if len(self.ids.profiles_1d[0].q) < 1:
            logger.critical(
                "core_profiles.profiles_1d[" + str(sliceIndex) + "].q could not be read"
            )
            self.ids.profiles_1d[0].q = np.asarray([np.nan] * nrho)

        # Magnetic shear profile
        if len(self.ids.profiles_1d[0].magnetic_shear) < 1:
            logger.critical(
                "core_profiles.profiles_1d["
                + str(sliceIndex)
                + "].magnetic_shear could not be read"
            )
            self.ids.profiles_1d[0].magnetic_shear = np.asarray([np.nan] * nrho)

        if len(self.ids.profiles_1d[0].q) != nrho:
            logger.critical(
                "--------------------------------------------------------------"
            )
            logger.critical("Dimensions of input core profiles are not consistent:")
            logger.critical("  core_profiles.profiles_1d[0].grid.rho_tor(_norm)")
            logger.critical("  and core_profiles.profiles_1d[0].q")
            logger.critical("  have different dimensions:")
            logger.critical(
                f"- len(core_profiles.profiles_1d[0].grid.rho_tor(_norm))= {nrho}"
            )
            logger.critical(
                f"- len(core_profiles.profiles_1d[0].q = {len(self.ids.profiles_1d[0].q)}"
            )
            logger.critical("----> Aborted.")
            logger.critical(
                "--------------------------------------------------------------"
            )
            return None

        # Create the dictionary defining the list of profiles that can be displayed
        profiles = {}
        profiles["rhonorm"] = rhoTorNorm
        profiles["j_bootstrap"] = self.ids.profiles_1d[0].j_bootstrap
        profiles["j_non_inductive"] = self.ids.profiles_1d[0].j_non_inductive
        profiles["j_ohmic"] = self.ids.profiles_1d[0].j_ohmic
        profiles["j_total"] = self.ids.profiles_1d[0].j_total
        profiles["q"] = self.ids.profiles_1d[0].q
        profiles["magnetic_shear"] = self.ids.profiles_1d[0].magnetic_shear
        return profiles

    def getnrho(self, sliceIndex=0):
        nrho = None
        try:
            if len(self.ids.profiles_1d[sliceIndex].grid.rho_tor_norm) > 0:
                nrho = len(self.ids.profiles_1d[sliceIndex].grid.rho_tor_norm)
            elif len(self.ids.profiles_1d[sliceIndex].grid.rho_tor) > 0:
                nrho = len(self.ids.profiles_1d[sliceIndex].grid.rho_tor)
        except Exception as e:
            logger.warning(
                "core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor could not be read."
            )
        return nrho
