"""
This module provides compute functions and classes for core_profiles ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import contextlib
import functools
import itertools
import logging
from typing import Union

try:
    import imaspy as imas
except ImportError:
    import imas
import numpy as np

import idstools.init_mendeleiev as mend

logger = logging.getLogger("module")


class CoreProfilesCompute:
    def __init__(self, ids, volume=None):
        self.ids = ids
        self.volume = volume

    @staticmethod
    def get_plasma_composition_with_species_concentration(ids, time_slice, volume=None) -> Union[dict, int]:
        """
        Function retrives composition and species concentration in below format
        """
        try:
            _ = ids.profiles_1d[time_slice]

        except Exception as e:
            logger.debug(f"{e}")
            return 0

        core_profile_compute = CoreProfilesCompute(ids, volume=volume)

        if core_profile_compute.volume is None:
            volume = core_profile_compute.get_volume(time_slice)
            if volume is None:
                return -1
            else:
                core_profile_compute.volume = volume
        data = {}

        nspec_over_ntot = core_profile_compute.get_nspec_over_ntot(time_slice)
        nspec_over_ne = core_profile_compute.get_nspec_over_ne(time_slice)
        nspec_over_nmaj = core_profile_compute.get_nspec_over_nmaj(time_slice)
        species = core_profile_compute.get_species(time_slice)
        labels = core_profile_compute.get_labels(time_slice)
        core_profile_compute.combine_species_when_appear_twice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj, time_slice
        )
        a = core_profile_compute.get_a(time_slice)
        z = core_profile_compute.get_z(time_slice)
        states_data = core_profile_compute.get_states_data(time_slice)
        if species:
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
    def get_electron_density_ne0(self):
        """
        This function `get_electron_density_ne0` returns a list of electron densities at the
        first position for each time step in a given object.

        Returns:
            The function `get_ne0` returns a list of electron densities at the first spatial point (index 0) for all
            time steps in the simulation. The electron density is in units of 1e-19 m^-3.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=105033;run=1;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_electron_density_ne0(time_slice=0)

                [5.106128949975287]
        """
        ntime = len(self.ids.time)

        return [self.ids.profiles_1d[itime].electrons.density[0] * 1.0e-19 for itime in range(ntime)]

    @functools.lru_cache(maxsize=128)
    def get_a(self, time_slice, element_index=0) -> list:
        """
        This function returns a list of atomic masses for a given slice and element index.

        Args:
            time_slice (int, optional): The index of the slice in the `ggd` list that contains the ion
                information.Defaults to 0
            element_index (int, optional): Element index, It is used to access the 'a' attribute of
                the element object. Defaults to 0

        Returns:
            a list of atomic masses for each species in the given slice index and element index.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=105033;run=1;database=ITER;version=3", "r")

                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_a(time_slice=0)

                [2.0, 3.0, 4.0, 9.0, 183.84, 40.0, 20.0]
        """
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        a = [0] * nspecies
        for ispecies in range(nspecies):
            a[ispecies] = self.ids.profiles_1d[time_slice].ion[ispecies].element[element_index].a
        logger.debug(f"Mass of atom : {a}")
        return a

    @functools.lru_cache(maxsize=128)
    def get_z(self, time_slice: int, element_index: int = 0) -> list:
        """
        This function `get_z` returns a list of nuclear charges for each species in a given slice and element
        index.

        Args:
            time_slice (int, optional): time slice on which functions should operate on. Defaults to 0.
            element_index (int, optional): element of the atom or molecule on which functions should operate on.
                Defaults to 0.

        Returns:
            a list of nuclear charges for each species in the given time_slice and elementIndex.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=105033;run=1;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_z(time_slice=0)

                [1, 1, 2, 4, 74, 18, 10]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        z = [0] * nspecies
        for ispecies in range(nspecies):
            z[ispecies] = int(self.ids.profiles_1d[time_slice].ion[ispecies].element[element_index].z_n)
        logger.debug(f"Nuclear charge each species : {z}")
        return z

    def get_states(self, time_slice: int) -> list:
        """
        This function `get_states` returns quantities related to the different states of the species
        (ionisation, energy, excitation, ...) for each species

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of states (ionisation, energy, excitation, etc.) in  the input data of each species .

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=105033;run=1;database=ITER;version=3", "r")

                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_states(time_slice=0)

                print(result[0]) # state object from species

        """
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        return [self.ids.profiles_1d[time_slice].ion[species_index].state for species_index in range(nspecies)]

    def get_state_density(
        self, time_slice: int, species_index: int = 0, state_index: int = 0
    ) -> Union[np.ndarray, None]:
        """
        This function `get_state_density` returns the density of a specified state of a
        specified species at a specified time slice, or the thermal density if the former is not available.

        Args:
            time_slice (int): an integer representing the index of the time slice for which the density is being
                requested. Defaults to 0
            species_index (int): The index of the ion species for which the density is being retrieved. Defaults to 0
            state_index (int): The index of the state for which the density is being retrieved. Defaults to 0

        Returns:
            a numpy array containing the density of a specified state of a specified species at a specified time slice.
            If the density is not available, it returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_state_density(time_slice, speciesIndex=0, stateIndex=0)

                array([4.16759116e+19, 4.17266130e+19, 4.17275806e+19, 4.17086410e+19,
                4.16751781e+19, 4.16983762e+19, 4.17344996e+19, 4.17944658e+19,
        """
        with contextlib.suppress(Exception):
            density = self.ids.profiles_1d[time_slice].ion[species_index].state[state_index].density
            if len(density) != 0:
                return density
        with contextlib.suppress(Exception):
            density = self.ids.profiles_1d[time_slice].ion[species_index].state[state_index].density_thermal
            if len(density) != 0:
                return density
        return None

    def get_states_data(self, time_slice: int) -> dict:
        """
        This function `get_states_data` returns a dictionary containing data on the states and densities of different
        species in a plasma simulation.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a dictionary containing information about the states of different species in a plasma, including
            their labels, z-averages, densities, and relative densities.


        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_states_data(time_slice=0)


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

        volume = self.get_volume(time_slice)
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        species_density, _, _ = self.get_species_density(time_slice)
        states_data = {}
        for species_index in range(nspecies):
            logger.debug(f"Species index :{species_index}")
            logger.debug(f"Species density :{species_density[species_index]}")
            species_data = {}
            nstates = len(self.ids.profiles_1d[time_slice].ion[species_index].state)
            logger.debug(f"Species states count :{nstates}")
            states_density = [0] * nstates
            for state_index in range(nstates):
                if hasattr(self.ids.profiles_1d[time_slice].ion[species_index], "label"):
                    ion_name = self.ids.profiles_1d[time_slice].ion[species_index].label
                elif hasattr(self.ids.profiles_1d[time_slice].ion[species_index], "name"):
                    ion_name = self.ids.profiles_1d[time_slice].ion[species_index].name

                if hasattr(self.ids.profiles_1d[time_slice].ion[species_index].state[state_index], "label"):
                    state_name = self.ids.profiles_1d[time_slice].ion[species_index].state[state_index].label
                elif hasattr(self.ids.profiles_1d[time_slice].ion[species_index].state[state_index], "name"):
                    state_name = self.ids.profiles_1d[time_slice].ion[species_index].state[state_index].name
                state_data = {
                    "label": state_name,
                    "z_average": np.mean(
                        self.ids.profiles_1d[time_slice].ion[species_index].state[state_index].z_average
                    ),
                }

                density = self.get_state_density(time_slice, species_index, state_index)
                state_data["density_available"] = False
                if density is None:
                    logger.critical(
                        f"core_profile IDS: Density data for species"
                        f"{ion_name} and state"
                        f"{str(state_index)} is empty"
                    )
                elif len(density) != 0:
                    # if all density values in the array are 1.0 or 0.0 then do not calculate
                    # because it can be false values
                    if np.all(density == 1.0) or np.all(density == 0.0):
                        logger.critical(
                            f"core_profile IDS: Density data for species"
                            f"{ion_name}"
                            f"and state {str(state_index)} all are ones or zeros"
                        )
                    else:
                        logger.debug(f"Density array :{density}")
                        states_density[state_index] = sum(density * volume)
                        state_data["density_available"] = True
                else:
                    logger.critical(
                        f"core_profile IDS: Density data for species" f"{ion_name}" f" and state {state_index} is empty"
                    )
                # TODO Couldn't retrive state desnity should we calculate n/ni?
                # In that case density is always 0 and no meaning of n/ni
                # We can also get weired errors
                #  idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning:
                # invalid value encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                # idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning:
                # divide by zero encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                state_data["states_density"] = states_density
                logger.debug(
                    f"State density at index {state_index} : State density : {states_density[state_index]}"
                    + "\t Species density :"
                    + str(species_density[species_index])
                )
                # if species density is 0.0 then do not calculate n/ni
                if species_density[species_index] != 0.0:
                    state_data["n_ni"] = 100 * states_density[state_index] / species_density[species_index]
                else:
                    state_data["n_ni"] = 0.0
                species_data[str(state_index)] = state_data

            # label = self.ids_object.profiles_1d[time_slice].ion[species_index].label
            states_data[str(species_index)] = species_data
        return states_data

    def get_ne(self, time_slice: int) -> float:
        """
        This function `get_ne` calculates the total number of electrons (ne) based on the volume and electron density
        of a given slice.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the total number of electrons (ne) in the given slice of the object, calculated by multiplying the
            volume of the slice with its electron density and summing the results.

        Example:
            .. code-block:: python

            import imas
            connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
            idsObj = connection.get('core_profiles')
            connection.close()
            computeObj = CoreProfilesCompute(idsObj)
            result = computeObj.get_ne(time_slice=0)

            8.778296205101714e+23
        """
        volume = self.get_volume(time_slice)

        electron_density = self.ids.profiles_1d[time_slice].electrons.density
        logger.info(f"Total no. electrons (ne): {str(sum(volume * electron_density))}")
        return sum(volume * electron_density)

    @functools.lru_cache(maxsize=128)
    def get_volume(self, time_slice: int) -> np.ndarray:
        """
        This function `get_volume` returns the volume of a grid at a given time slice.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the volume of the grid for a given time slice. If the volume is empty, it returns None

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_volume(time_slice=0)

                array([4.39932160e-02, 2.19952424e-01, 5.71837023e-01, 1.09958863e+00,
                1.80311391e+00, 2.68234060e+00, 3.73724537e+00, 4.96778828e+00,
        """
        volume = self.ids.profiles_1d[time_slice].grid.volume
        if len(volume) == 0:
            volume = None
            logger.critical("core_profile IDS: Grid volume is empty")
        logger.info(f"Total volume:{np.sum(volume)}")
        return volume

    @functools.lru_cache(maxsize=128)
    def get_species_density(self, time_slice: int) -> tuple:
        """
        This function calculates the density of different species in a given slice and returns a tuple
        containing the species density list, the total density, and the index of the species with the maximum density.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a tuple containing three values: a list of species density, the total density of all species, and the
            index of the species with the maximum density.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                connection.close()
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_species_density(time_slice=0)

                ([6.50016400579169e+23, 8.289108520803897e+22, 6.202712465391594e+21],7.391101982525995e+23, 0)
        """
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        sum_density = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            volume = self.get_volume(time_slice)
            density = self.ids.profiles_1d[time_slice].ion[ispecies].density
            species_density_list[ispecies] = sum(volume * density)

            sum_density = sum_density + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
        logger.debug(f"Species density:{str(species_density_list)}")
        return species_density_list, sum_density, max_density_index

    def get_nspec_over_ntot(self, time_slice: int):
        """
        This function calculates the ratio of the number of species to the total number of particles in a plasma.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            The function `get_nspec_over_ntot` is returning the ratio of the list of species densities to the
            total density (`ntot`).

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_nspec_over_ntot(time_slice=0)

                array([0.87945803, 0.11214983, 0.00839213])
        """
        species_density_list, sum_density, _ = self.get_species_density(time_slice)
        return species_density_list / sum_density

    def get_nspec_over_ne(self, time_slice: int):
        """
        This function calculates the ratio of species density to electron density.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            the ratio of the species density list to the electron density (ne).

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_nspec_over_ne(time_slice=0)

                array([0.74048128, 0.0944273 , 0.00706596])
        """
        species_density_list, _, _ = self.get_species_density(time_slice)
        ne = self.get_ne(time_slice)
        return species_density_list / ne

    def get_nspec_over_nmaj(self, time_slice: int) -> list:
        """
        This function returns a list of the ratio of each species density to the maximum species density.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of values obtained by dividing each element of the list `species_density_list` by the maximum
            value in that list. This list represents the ratio of the density of each species to the density
            of the most abundant species.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_nspec_over_nmaj(time_slice=0)

                array([1.        , 0.12752153, 0.00954239])
        """
        (
            species_density_list,
            _,
            max_density_index,
        ) = self.get_species_density(time_slice)
        return species_density_list / species_density_list[max_density_index]

    def get_species(self, time_slice: int) -> list:
        """
        This function `get_species` creates a Mendeleiev table and returns a list of species based on the
        values of a, z,   and the table.

        Args:
            time_slice (int, optional): time slice on which function should operate on. Defaults to 0.

        Returns:
            a list of species based on the values of a, z, and the Mendeleev table.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_species(time_slice=0)

                ['H', 'He4', 'Ne']
        """
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids.profiles_1d[time_slice].ion)

        a = list(map(int, self.get_a(time_slice)))
        z = list(map(int, self.get_z(time_slice)))
        if any(value == imas.ids_defs.EMPTY_INT for value in z):
            logger.error(
                f"core_profiles.profiles_1d[{time_slice}].ion[].element[].z_n" f" values are not available {z}"
            )
            return None
        return [table_mendeleiev[z[ispecies]][a[ispecies]].element for ispecies in range(nspecies)]

    def get_labels(self, time_slice: int) -> list:
        """
        This function `get_labels` returns a list of labels for all species in a given time slice.

        Args:
            time_slice: an optional integer parameter that specifies the time slice on which the function should
                operate. The default value is 0

        Returns:
            a list of labels for all species in a given time slice.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_labels(time_slice=0)

                ['H', 'He', 'Ne']
        """
        nspecies = len(self.ids.profiles_1d[time_slice].ion)
        if hasattr(self.ids.profiles_1d[time_slice].ion[0], "label"):
            labels = [self.ids.profiles_1d[time_slice].ion[ispecies].label for ispecies in range(nspecies)]
        elif hasattr(self.ids.profiles_1d[time_slice].ion[0], "name"):
            labels = [self.ids.profiles_1d[time_slice].ion[ispecies].name for ispecies in range(nspecies)]

        logger.debug(f"Species identification :{labels}")
        return labels

    def combine_species_when_appear_twice(self, species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj, time_slice):
        """
        This is helper function which checks if there are duplicate entries of species and combine the species.
        This is in place change of arrays

        Args:
            species (list): result from get_species()
            nspec_over_ntot (list): result from get_nspec_over_ntot()
            nspec_over_ne (list): result from get_nspec_over_ne()
            nspec_over_nmaj (list): result from get_nspec_over_nmaj()
            time_slice (int, optional): time_slice on which function should operate on. Defaults to 0.
        """
        if species is not None:
            nspecies = len(self.ids.profiles_1d[time_slice].ion)
            for ispecies, jspecies in itertools.product(range(nspecies), range(nspecies)):
                if (species[jspecies] == species[ispecies]) & (jspecies != ispecies):
                    nspec_over_ntot[ispecies] = nspec_over_ntot[ispecies] + nspec_over_ntot[jspecies]
                    nspec_over_ntot[jspecies] = 0
                    nspec_over_ne[ispecies] = nspec_over_ne[ispecies] + nspec_over_ne[jspecies]
                    nspec_over_ne[jspecies] = 0
                    nspec_over_nmaj[ispecies] = nspec_over_nmaj[ispecies] + nspec_over_nmaj[jspecies]
                    nspec_over_nmaj[jspecies] = 0

    def get_rho_tor_norm(self, time_slice: int) -> Union[np.ndarray, None]:
        """
        This function `get_rho_tor_norm` returns a list of normalized toroidal rho values from a given
        time slice of a profiles_1d object.

        Args:
            time_slice (int): time index. Defaults to 0

        Returns:
            a list of normalized toroidal flux coordinates (rho_tor_norm) for a given time slice of the IDS object.
            If rho_tor_norm is not available, it tries to return a list of toroidal flux coordinates (rho_tor) instead.
            If neither is available, it returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_rho_tor_norm(time_slice=0)

                [0.005025125628140704,
                0.015075376884422112,
                0.035175879396984924,
                0.045226130653266326,
                0.05527638190954774]
        """
        try:
            if len(self.ids.profiles_1d[time_slice].grid.rho_tor_norm) > 0:
                return self.ids.profiles_1d[time_slice].grid.rho_tor_norm
            elif len(self.ids.profiles_1d[time_slice].grid.rho_tor) > 0:
                return self.ids.profiles_1d[time_slice].grid.rho_tor / self.ids.profiles_1d[time_slice].grid.rho_tor[-1]
        except IndexError:
            logger.error(f"core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm or rho_tor is not available")
        return None

    def get_psi(self, time_slice: int) -> Union[list, None]:
        """
        This function `get_psi` returns the poloidal magnetic flux (psi) at a given time slice.

        Args:
            time_slice (int): time index

        Returns:
            the poloidal magnetic flux (psi) as a list of floats for a given time slice. If the length of the
            poloidal magnetic flux is greater than 0, then the function returns the negative of the poloidal
            magnetic flux. If the length of the poloidal magnetic flux is 0, then the function returns None.

        Example:
            .. code-block:: python

                import imas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=104010;run=2;database=ITER;version=3", "r")
                idsObj = connection.get('core_profiles')
                computeObj = CoreProfilesCompute(idsObj)
                result = computeObj.get_psi(time_slice=0)

                array([-4.95660880e+01, -4.95537345e+01, -4.95275298e+01, -4.94833135e+01,
                -4.94209348e+01, -4.93461904e+01, -4.92595767e+01, -4.91573223e+01,
        """
        psi = None
        if len(self.ids.profiles_1d[time_slice].grid.psi) > 0:
            psi = -self.ids.profiles_1d[time_slice].grid.psi
        return psi

    def get_ion_pressure_properties(self, time_slice):
        """
        The `get_ion_pressure_properties` function calculates and returns the total thermal pressure,
        fast parallel pressure, and fast perpendicular pressure of ions in a given set of profiles.

        Returns:
            The function `get_ion_pressure_properties` is returning a dictionary containing the following
        keys and values: maxima_ion, pressure_ion_thermal, pressure_ion_fast_parallel, pressure_ion_fast_perpendicular
        """
        nrho = len(self.get_rho_tor_norm(time_slice))
        pressure_ion_thermal = 0.0
        pressure_ion_fast_parallel = 0.0
        pressure_ion_fast_perpendicular = 0.0
        for ion in self.ids.profiles_1d[time_slice].ion:
            if len(ion.pressure_thermal) == 0:
                logger.warning(f"Empty profiles_1d[{time_slice}].ion.pressure_thermal")
            if len(ion.pressure_fast_parallel) == 0:
                logger.warning(f"Empty profiles_1d[{time_slice}].ion.pressure_fast_parallel")
            if len(ion.pressure_fast_perpendicular) == 0:
                logger.warning(f"Empty profiles_1d[{time_slice}].ion.pressure_fast_perpendicular")
            pressure_ion_thermal = pressure_ion_thermal + ion.pressure_thermal
            pressure_ion_fast_parallel = (
                pressure_ion_fast_parallel + np.asarray([np.nan] * nrho)
                if len(ion.pressure_fast_parallel) == 0
                else ion.pressure_fast_parallel
            )
            pressure_ion_fast_perpendicular = (
                pressure_ion_fast_perpendicular + np.asarray([np.nan] * nrho)
                if len(ion.pressure_fast_perpendicular) == 0
                else ion.pressure_fast_perpendicular
            )

        pressure_ion_thermal = np.asarray([np.nan] * nrho) if len(pressure_ion_thermal) == 0 else pressure_ion_thermal
        pressure_ion_fast_parallel = (
            np.asarray([np.nan] * nrho) if len(pressure_ion_fast_parallel) == 0 else pressure_ion_fast_parallel
        )
        pressure_ion_fast_perpendicular = (
            np.asarray([np.nan] * nrho)
            if len(pressure_ion_fast_perpendicular) == 0
            else pressure_ion_fast_perpendicular
        )

        maxima_ion = max(
            np.nan_to_num(max(pressure_ion_thermal[: nrho - 1])),
            np.nan_to_num(max(pressure_ion_fast_parallel[: nrho - 1])),
            np.nan_to_num(max(pressure_ion_fast_perpendicular[: nrho - 1])),
        )
        maxima_ion = maxima_ion * 1.1
        return {
            "maxima_ion": maxima_ion,
            "pressure_ion_thermal": pressure_ion_thermal,
            "pressure_ion_fast_parallel": pressure_ion_fast_parallel,
            "pressure_ion_fast_perpendicular": pressure_ion_fast_perpendicular,
        }

    def get_electrons_pressure_properties(self, time_slice):
        """
        The  function `get_electrons_pressure_properties` calculates and returns various pressure properties
        of electrons, including maximum pressure and individual pressure components.

        Returns:
            The `get_electrons_pressure_properties` function returns a dictionary with the following
            key-value pairs:
            "maxima_electrons": Maximum pressure of electrons
            "pressure_electron_total": Total pressure of electrons
            "pressure_electron_thermal": Thermal pressure of electrons
            "pressure_electron_fast_parallel": Pressure of fast parallel electrons
            "pressure_electron_fast_perpendicular

        """
        nrho = len(self.get_rho_tor_norm(time_slice))
        pressure_electron_total = self.ids.profiles_1d[time_slice].electrons.pressure
        pressure_electron_thermal = self.ids.profiles_1d[time_slice].electrons.pressure_thermal
        pressure_electron_fast_parallel = self.ids.profiles_1d[time_slice].electrons.pressure_fast_parallel
        pressure_electron_fast_perpendicular = self.ids.profiles_1d[time_slice].electrons.pressure_fast_perpendicular
        if len(pressure_electron_total) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].electrons.pressure")
        if len(pressure_electron_thermal) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].electrons.pressure_thermal")
        if len(pressure_electron_fast_parallel) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].electrons.pressure_fast_parallel")
        if len(pressure_electron_fast_perpendicular) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].electrons.pressure_fast_perpendicular")
        pressure_electron_total = (
            np.asarray([np.nan] * nrho) if len(pressure_electron_total) == 0 else pressure_electron_total
        )
        pressure_electron_thermal = (
            np.asarray([np.nan] * nrho) if len(pressure_electron_thermal) == 0 else pressure_electron_thermal
        )
        pressure_electron_fast_parallel = (
            np.asarray([np.nan] * nrho)
            if len(pressure_electron_fast_parallel) == 0
            else pressure_electron_fast_parallel
        )
        pressure_electron_fast_perpendicular = (
            np.asarray([np.nan] * nrho)
            if len(pressure_electron_fast_perpendicular) == 0
            else pressure_electron_fast_perpendicular
        )

        maxima_electrons = max(
            np.nan_to_num(max(pressure_electron_total[: nrho - 1])),
            np.nan_to_num(max(pressure_electron_thermal[: nrho - 1])),
            np.nan_to_num(max(pressure_electron_fast_parallel[: nrho - 1])),
            np.nan_to_num(max(pressure_electron_fast_perpendicular[: nrho - 1])),
        )
        maxima_electrons = maxima_electrons * 1.1
        return {
            "maxima_electrons": maxima_electrons,
            "pressure_electron_total": pressure_electron_total,
            "pressure_electron_thermal": pressure_electron_thermal,
            "pressure_electron_fast_parallel": pressure_electron_fast_parallel,
            "pressure_electron_fast_perpendicular": pressure_electron_fast_perpendicular,
        }

    def get_pressure(self, time_slice):
        """
        The function `get_pressure` returns a dictionary containing the thermal pressure, parallel pressure,
        and perpendicular pressure.

        Returns:
            The `get_pressure` function returns a dictionary with the following key-value pairs:
            "maxima_total": maximum value calculated based on pressure values
            "pressure_total": total pressure value calculated as the sum of electron pressure and ion pressure
            "pressure_thermal": thermal pressure values
            "pressure_parallel": parallel pressure values
            "pressure_perpendicular": perpendicular pressure values
        """
        nrho = len(self.get_rho_tor_norm(time_slice))
        pressure_thermal = self.ids.profiles_1d[time_slice].pressure_thermal
        pressure_parallel = self.ids.profiles_1d[time_slice].pressure_parallel
        pressure_perpendicular = self.ids.profiles_1d[time_slice].pressure_perpendicular
        if len(pressure_thermal) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].pressure_thermal")
        if len(pressure_parallel) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].pressure_fast_parallel")
        if len(pressure_perpendicular) == 0:
            logger.warning(f"Empty profiles_1d[{time_slice}].pressure_fast_perpendicular")
        pressure_thermal = np.asarray([np.nan] * nrho) if len(pressure_thermal) == 0 else pressure_thermal
        pressure_parallel = np.asarray([np.nan] * nrho) if len(pressure_parallel) == 0 else pressure_parallel
        pressure_perpendicular = (
            np.asarray([np.nan] * nrho) if len(pressure_perpendicular) == 0 else pressure_perpendicular
        )

        dict_electrons_pressure_properties = self.get_electrons_pressure_properties(time_slice)
        pressure_electron_total = dict_electrons_pressure_properties["pressure_electron_total"]

        pressure_ion_total = self.get_pressure_ion_total(time_slice)
        pressure_total = np.copy(pressure_electron_total)
        if pressure_ion_total is not None:
            pressure_total += pressure_ion_total

        # Minima and maxima calculations for plots
        maxima_total = max(
            np.nan_to_num(max(pressure_total[: nrho - 1])),
            np.nan_to_num(max(pressure_thermal[: nrho - 1])),
            np.nan_to_num(max(pressure_parallel[: nrho - 1])),
            np.nan_to_num(max(pressure_perpendicular[: nrho - 1])),
        )

        maxima_total = maxima_total * 1.1

        return {
            "maxima_total": maxima_total,
            "pressure_total": pressure_total,
            "pressure_thermal": pressure_thermal,
            "pressure_parallel": pressure_parallel,
            "pressure_perpendicular": pressure_perpendicular,
        }

    def get_pressure_ion_total(self, time_slice) -> Union[float, None]:
        """
        The function `get_pressure_ion_total` returns the total ion pressure from a given set of
        profiles or None if the pressure values cannot be read.

        Returns:
            The function `get_pressure_ion_total` returns the total ion pressure from a given set of
        profiles, or `None` if the pressure values cannot be read.
        """
        pressure_ion_total = None
        if len(self.ids.profiles_1d[time_slice].pressure_ion_total) > 1:
            pressure_ion_total = self.ids.profiles_1d[time_slice].pressure_ion_total
        else:
            logger.critical(
                f"core_profiles.profiles_1d[{time_slice}].pressure_ion_total could not be read",
            )
            if len(self.ids.profiles_1d[time_slice].ion[0].pressure) > 1:
                pressure_ion_total = 0.0
                for ion in self.ids.profiles_1d[time_slice].ion:
                    pressure_ion_total = pressure_ion_total + ion.pressure
            else:
                logger.critical(
                    f"core_profiles.profiles_1d[{time_slice}].ion[0].pressure could not be read",
                )
        return pressure_ion_total

    def get_profiles(self, time_slice):
        """
        The function `get_profiles` retrieves and organizes various profiles from a data source for
        further analysis.

        Args:
            time_slice: The `time_slice` parameter in the `get_profiles` method is used to specify which
                slice of profiles to retrieve.

        Returns:
            A dictionary named `profiles` is being returned, which contains the following keys and
            corresponding values
        """
        rho_tor_norm = self.get_rho_tor_norm(time_slice)
        if rho_tor_norm is None:
            logger.critical("core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty")
            logger.critical("----> Aborted.")
            return None

        nrho = len(rho_tor_norm)

        # J_bootstrap profile
        j_bootstrap = self.ids.profiles_1d[time_slice].j_bootstrap
        if len(self.ids.profiles_1d[time_slice].j_bootstrap) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].j_bootstrap could not be read")
            j_bootstrap = np.asarray([np.nan] * nrho)

        # J_non_inductive profile
        j_non_inductive = self.ids.profiles_1d[time_slice].j_non_inductive
        if len(self.ids.profiles_1d[time_slice].j_non_inductive) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].j_non_inductive could not be read")
            j_non_inductive = np.asarray([np.nan] * nrho)

        # J_ohmic profile
        j_ohmic = self.ids.profiles_1d[time_slice].j_ohmic
        if len(self.ids.profiles_1d[time_slice].j_ohmic) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].j_ohmic could not be read")
            j_ohmic = np.asarray([np.nan] * nrho)

        # J_total profile
        j_total = self.ids.profiles_1d[time_slice].j_total
        if len(self.ids.profiles_1d[time_slice].j_total) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].j_total could not be read")
            j_total = np.asarray([np.nan] * nrho)

        # q-profile
        q = self.ids.profiles_1d[time_slice].q
        if len(self.ids.profiles_1d[time_slice].q) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].q could not be read")
            q = np.asarray([np.nan] * nrho)

        # Magnetic shear profile
        magnetic_shear = self.ids.profiles_1d[time_slice].magnetic_shear
        if len(self.ids.profiles_1d[time_slice].magnetic_shear) < 1:
            logger.critical("core_profiles.profiles_1d[" + str(time_slice) + "].magnetic_shear could not be read")
            magnetic_shear = np.asarray([np.nan] * nrho)

        if len(self.ids.profiles_1d[time_slice].q) != nrho:
            logger.critical("--------------------------------------------------------------")
            logger.critical("Dimensions of input core profiles are not consistent:")
            logger.critical(f"  core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm)")
            logger.critical(f"  and core_profiles.profiles_1d[{time_slice}].q")
            logger.critical("  have different dimensions:")
            logger.critical(f"- len(core_profiles.profiles_1d[{time_slice}].grid.rho_tor_norm))= {nrho}")
            logger.critical(
                f"- len(core_profiles.profiles_1d[{time_slice}].q = {len(self.ids.profiles_1d[time_slice].q)}"
            )
            logger.critical("----> Aborted.")
            logger.critical("--------------------------------------------------------------")
            return None

        # Create the dictionary defining the list of profiles that can be displayed
        profiles = {}
        profiles["rhonorm"] = rho_tor_norm
        profiles["j_bootstrap"] = j_bootstrap
        profiles["j_non_inductive"] = j_non_inductive
        profiles["j_ohmic"] = j_ohmic
        profiles["j_total"] = j_total
        profiles["q"] = q
        profiles["magnetic_shear"] = magnetic_shear
        return profiles

    def getnrho(self, time_slice):
        """
        This function `getnrho` returns the number of elements in the `rho_tor_norm` or `rho_tor` grid
        based on the provided slice index.

        Args:
            time_slice: The `time_slice` parameter in the `getnrho` method is used to specify which
                slice of data to retrieve the number of rho values from.

        Returns:
            The `getnrho` method is returning the number of elements in the `rho_tor_norm` or `rho_tor`
            attribute of the `grid` object within the `profiles_1d` object at the specified `time_slice`.
            If either of these attributes has elements, the length of that attribute is returned as the
            number of `nrho`.
        """
        nrho = None
        try:
            if len(self.ids.profiles_1d[time_slice].grid.rho_tor_norm) > 0:
                nrho = len(self.ids.profiles_1d[time_slice].grid.rho_tor_norm)
            elif len(self.ids.profiles_1d[time_slice].grid.rho_tor) > 0:
                nrho = len(self.ids.profiles_1d[time_slice].grid.rho_tor)
        except Exception as e:
            logger.debug(f"{e}")
            logger.warning(f"core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor could not be read. {e}")
        return nrho
