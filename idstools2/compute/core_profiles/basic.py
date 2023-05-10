#  src/compute/core_profiles/functions.py ok

import numpy as np
import database_tools.init_mendeleiev as mend
import sys
import logging
import functools

logger = logging.getLogger("module." + __name__)


class CoreProfilesCompute:
    def __init__(self, ids_object, slice_index=0, volume=None):
        super().__init__()
        self.ids_object = ids_object
        self.slice_index = slice_index
        self.volume = volume

    @staticmethod
    def get_plasma_composition_with_species_concentration(
        ids_object, slice_index=0, volume=None
    ) -> dict:
        """
        Function retrives composition and species concentration in below format
        """
        try:
            ids_object.profiles_1d[slice_index]

        except:
            return 0

        coreProfileCompute = CoreProfilesCompute(ids_object, slice_index, volume=volume)

        if coreProfileCompute.volume is None:
            volume = coreProfileCompute.get_volume(slice_index)
            if volume is None:
                return -1
            else:
                coreProfileCompute.volume = volume
        data = {}

        nspec_over_ntot = coreProfileCompute.get_nspec_over_ntot()
        nspec_over_ne = coreProfileCompute.get_nspec_over_ne()
        nspec_over_nmaj = coreProfileCompute.get_nspec_over_nmaj()
        species = coreProfileCompute.get_species()
        labels = coreProfileCompute.get_labels()
        coreProfileCompute.combine_species_when_appear_twice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj
        )
        a = coreProfileCompute.get_a()
        z = coreProfileCompute.get_z()
        states_data = coreProfileCompute.get_states_data()
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

    @functools.lru_cache(maxsize=128)
    def get_ne0(self):
        ntime = len(self.ids_object.time)

        ne0 = []
        for itime in range(ntime):
            ne0.append(
                self.ids_object.profiles_1d[itime].electrons.density[0] * 1.0e-19
            )
        return ne0

    @functools.lru_cache(maxsize=128)
    def get_a(self, slice_index=0, element_index=0) -> list:
        """
        Get series wise value of a of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            element_index (int, optional): [element on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise values of [a] of all species ]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        a = [0] * nspecies
        for ispecies in range(nspecies):
            a[ispecies] = (
                self.ids_object.profiles_1d[slice_index]
                .ion[ispecies]
                .element[element_index]
                .a
            )
        logger.debug("Mass of atom : " + str(a))
        return a

    @functools.lru_cache(maxsize=128)
    def get_z(self, slice_index=0, element_index=0) -> list:
        """
        Get series wise value of z of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            element_index (int, optional): [element on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise values of [z] of all species ]
        """
        # TODO why always element_index = 0 we are picking up
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        z = [0] * nspecies
        for ispecies in range(nspecies):
            z[ispecies] = int(
                self.ids_object.profiles_1d[slice_index]
                .ion[ispecies]
                .element[element_index]
                .z_n
            )
        logger.debug("Nuclear charge each species : " + str(z))
        return z

    # TODO Removed this method as it is not used anywhere
    # def get_zeff(self, slice_index=0, element_index=0):
    #     return self.ids_object.profiles_1d[slice_index].zeff[element_index]

    def get_states(self, slice_index=0, state_index=0):
        """
        Get series wise data of states of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [list]: [series wise data of states of all species ]
        """
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        states = []
        for species_index in range(nspecies):
            states.append(
                self.ids_object.profiles_1d[slice_index].ion[species_index].state
            )
        return states

    def get_state_density(self, slice_index=0, species_index=0, state_index=0):
        try:
            density = (
                self.ids_object.profiles_1d[slice_index]
                .ion[species_index]
                .state[state_index]
                .density
            )
            if len(density) != 0:
                return density
        except:
            pass

        try:
            density = (
                self.ids_object.profiles_1d[slice_index]
                .ion[species_index]
                .state[state_index]
                .density_thermal
            )
            if len(density) != 0:
                return density
        except:
            pass

        return None

    def get_states_data(self, slice_index=0) -> dict:
        """
        Get data of states in dictionary format

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [dict]: [data of states in dictionary format]
        """

        states_data = {}

        volume = self.get_volume(slice_index)
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        species_density, _, _ = self.get_species_density()
        for species_index in range(nspecies):
            logger.debug("Species index :" + str(species_index))
            logger.debug("Species density :" + str(species_density[species_index]))
            species_data = {}
            nstates = len(
                self.ids_object.profiles_1d[slice_index].ion[species_index].state
            )
            logger.debug("Species states count :" + str(nstates))
            states_density = [0] * nstates
            for state_index in range(nstates):
                state_data = {}

                state_data["label"] = (
                    self.ids_object.profiles_1d[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .label
                )

                state_data["z_average"] = np.mean(
                    self.ids_object.profiles_1d[slice_index]
                    .ion[species_index]
                    .state[state_index]
                    .z_average
                )

                density = self.get_state_density(
                    slice_index, species_index, state_index
                )
                state_data["density_available"] = False
                if density is not None:
                    if len(density) != 0:
                        # if all density values in the array are 1.0 or 0.0 then do not calculate because it can be false values
                        if np.all(density == 1.0) or np.all(density == 0.0):
                            logger.critical(
                                "core_profile IDS: Density data for species "
                                + self.ids_object.profiles_1d[slice_index]
                                .ion[species_index]
                                .label
                                + " and state "
                                + str(state_index)
                                + " all are ones or zeros "
                            )
                        else:
                            logger.debug("Density array :" + str(density))
                            states_density[state_index] = sum(density * volume)
                            state_data["density_available"] = True
                    else:
                        logger.critical(
                            "core_profile IDS: Density data for species "
                            + self.ids_object.profiles_1d[slice_index]
                            .ion[species_index]
                            .label,
                            " and state " + str(state_index) + " is empty ",
                        )
                else:
                    logger.critical(
                        "core_profile IDS: Density data for species "
                        + self.ids_object.profiles_1d[slice_index]
                        .ion[species_index]
                        .label
                        + " and state "
                        + str(state_index)
                        + " is empty "
                    )
                # TODO Couldn't retrive state desnity should we calculate n/ni?
                # In that case density is always 0 and no meaning of n/ni
                # We can also get weired errors
                #  /home/ITER/sawantp1/imasrepo/checkinfolder/idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: invalid value encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                # /home/ITER/sawantp1/imasrepo/checkinfolder/idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: divide by zero encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                state_data["states_density"] = states_density
                logger.debug(
                    "State density at index "
                    + str(state_index)
                    + " : State density : "
                    + str(states_density[state_index])
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

            # label = self.ids_object.profiles_1d[slice_index].ion[species_index].label
            states_data[str(species_index)] = species_data
        return states_data

    def get_ne(self, slice_index=0) -> float:
        """
        Sum of multiplication of volume and elcetrons density

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [float]: [Sum of multiplication of volume and elcetrons density ]
        """
        volume = self.get_volume(slice_index)

        electron_density = self.ids_object.profiles_1d[slice_index].electrons.density
        logger.info("Total no. electrons (ne): " + str(sum(volume * electron_density)))
        return sum(volume * electron_density)

    @functools.lru_cache(maxsize=128)
    def get_volume(self, slice_index=0):
        volume = self.ids_object.profiles_1d[slice_index].grid.volume
        if len(volume) == 0:
            volume = None
            logger.critical("core_profile IDS: Grid volume is empty")
        logger.info("Total volume:" + str(np.sum(volume)))
        return volume

    @functools.lru_cache(maxsize=128)
    def get_species_density(self, slice_index=0) -> tuple:
        """
        Returns species_density_list, sum_density, max_density_index of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            [float]: [species_density_list list of all species density]
            [float]: [sum_density Sum of densities]
            [float]: [max_density_index index at which it has maximum density]
        """
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        sum_density = 0
        species_density_list = [0] * nspecies
        max_density = -999.0
        max_density_index = 0
        for ispecies in range(nspecies):
            volume = self.get_volume(slice_index)
            density = self.ids_object.profiles_1d[slice_index].ion[ispecies].density
            species_density_list[ispecies] = sum(volume * density)

            sum_density = sum_density + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
        logger.debug("Species density:" + str(species_density_list))
        return species_density_list, sum_density, max_density_index

    def get_nspec_over_ntot(self):
        """
        Get series wise values of nspec_over_ntot

        Returns:
            [list]: [retruns list of series wise species property nspec_over_ntot]
        """
        species_density_list, sum_density, _ = self.get_species_density()
        return species_density_list / sum_density

    def get_nspec_over_ne(self):
        """
        Get series wise values of nspec_over_ne

        Returns:
            [list]: [retruns list of series wise species property nspec_over_ne]
        """
        species_density_list, _, _ = self.get_species_density()
        ne = self.get_ne()
        return species_density_list / ne

    def get_nspec_over_nmaj(self) -> list:
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

    def get_species(self, slice_index=0) -> list:
        """
        Creates mendeleiev table and put values of a anz z and return the series wise list of all species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            list: [Returns mendeleiev table and put values of a anz z and return the series wise list of all species]
        """
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)

        a = list(map(int, self.get_a()))
        z = list(map(int, self.get_z()))
        species = []
        for ispecies in range(nspecies):
            species.append(table_mendeleiev[z[ispecies]][a[ispecies]].element)
        return species

    def get_labels(self, slice_index=0) -> list:
        """
        Get label of species

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.

        Returns:
            list: [Returns species labels]
        """
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        labels = []
        for ispecies in range(nspecies):
            labels.append(self.ids_object.profiles_1d[slice_index].ion[ispecies].label)

        logger.debug("Species identification :" + str(labels))
        return labels

    def combine_species_when_appear_twice(
        self, species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj, slice_index=0
    ):
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
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
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

    def getRhoTorNorm(self, timeSlice: int = 0) -> list:
        """
        This function returns a list of normalized toroidal rho values from a given time slice of a profiles_1d object.

        Args:
            timeSlice (int): time index. Defaults to 0

        Returns:
            a list of normalized toroidal flux coordinates (rho_tor_norm) for a given time slice of the IDS object. If rho_tor_norm is not available, it tries to return a list of toroidal flux coordinates (rho_tor) instead. If neither is available, it returns None.
        """
        rhoTorNorm = None
        nrho = 0
        try:
            if len(self.ids_object.profiles_1d[timeSlice].grid.rho_tor_norm) > 0:
                nrho = len(self.ids_object.profiles_1d[timeSlice].grid.rho_tor_norm)
                rhoTorNorm = [0] * nrho
                for i in range(nrho):
                    rhoTorNorm[i] = self.ids_object.profiles_1d[
                        timeSlice
                    ].grid.rho_tor_norm[i]

                return rhoTorNorm
            elif len(self.ids_object.profiles_1d[timeSlice].grid.rho_tor) > 0:
                nrho = len(self.ids_object.profiles_1d[timeSlice].grid.rho_tor)
                rhoTorNorm = [0] * nrho
                for i in range(nrho):
                    rhoTorNorm[i] = (
                        self.ids_object.profiles_1d[timeSlice].grid.rho_tor[i]
                        / self.ids_object.profiles_1d[timeSlice].grid.rho_tor[nrho - 1]
                    )

                return rhoTorNorm

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
        """
        psi = None
        if len(self.ids_object.profiles_1d[timeSlice].grid.psi) > 0:
            psi = -self.ids_object.profiles_1d[timeSlice].grid.psi
        return psi
