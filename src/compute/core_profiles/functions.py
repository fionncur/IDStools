import numpy as np
import database_tools.init_mendeleiev as mend
import sys


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
        labels = coreProfileCompute.get_species_labels()
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

            data[str(species_index)] = species_data

        return data

    def get_ne0(self):
        ntime = len(self.ids_object.time)

        ne0 = []
        for itime in range(ntime):
            ne0.append(
                self.ids_object.profiles_1d[itime].electrons.density[0] * 1.0e-19
            )
        return ne0

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
            a[ispecies] = int(
                self.ids_object.profiles_1d[slice_index]
                .ion[ispecies]
                .element[element_index]
                .a
            )
        return a

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

        volume = self.volume
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        species_density, _, _ = self.get_species_density()
        for species_index in range(nspecies):
            species_data = {}
            nstates = len(
                self.ids_object.profiles_1d[slice_index].ion[species_index].state
            )
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
                        states_density[state_index] = sum(density * volume)
                        state_data["density_available"] = True
                    else:
                        print(
                            "!  core_profile IDS: Density data for species ",
                            self.ids_object.profiles_1d[slice_index]
                            .ion[species_index]
                            .label,
                            " and state ",
                            state_index,
                            " is empty ",
                        )
                else:
                    print(
                        "!  core_profile IDS: Density data for species ",
                        self.ids_object.profiles_1d[slice_index]
                        .ion[species_index]
                        .label,
                        " and state ",
                        state_index,
                        " is empty ",
                    )
                # TODO Couldn't retrive state desnity should we calculate n/ni?
                # In that case density is always 0 and no meaning of n/ni
                # We can also get weired errors
                #  /home/ITER/sawantp1/imasrepo/checkinfolder/idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: invalid value encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                # /home/ITER/sawantp1/imasrepo/checkinfolder/idstools/src/compute/core_profiles/functions.py:230: RuntimeWarning: divide by zero encountered in double_scalars
                #   100 * states_density[state_index] / species_density[species_index]
                state_data["states_density"] = states_density

                state_data["n_ni"] = (
                    100 * states_density[state_index] / species_density[species_index]
                )
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
        volume = self.volume

        electron_density = self.ids_object.profiles_1d[slice_index].electrons.density
        return sum(volume * electron_density)

    def get_nrho(self, time_index=0):
        nrho = None

        try:
            if len(self.ids_object.profiles_1d[time_index].grid.rho_tor_norm) > 0:
                nrho = len(self.ids_object.profiles_1d[time_index].grid.rho_tor_norm)
            elif len(self.ids_object.profiles_1d[time_index].grid.rho_tor) > 0:
                nrho = len(self.ids_object.profiles_1d[time_index].grid.rho_tor)
        except:
            print(
                "core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor could not be read.",
                file=sys.stderr,
            )
        if nrho == 0:
            print(
                "core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty.",
                file=sys.stderr,
            )
        return nrho

    def get_rho_tor_norm(self, time_index=0):
        # Normalized toroidal and poloidal flux coordinates
        rho_tor_norm = None
        nrho = self.get_nrho(time_index)
        if nrho != None:
            rho_tor_norm = [0] * nrho
            if len(self.ids_object.profiles_1d[time_index].grid.rho_tor_norm) > 0:
                for i in range(nrho):
                    rho_tor_norm[i] = self.ids_object.profiles_1d[
                        time_index
                    ].grid.rho_tor_norm[i]
            elif len(self.ids_object.profiles_1d[time_index].grid.rho_tor) > 0:
                for i in range(nrho):
                    rho_tor_norm[i] = (
                        self.ids_object.profiles_1d[time_index].grid.rho_tor[i]
                        / self.ids_object.profiles_1d[time_index].grid.rho_tor[nrho - 1]
                    )
        return rho_tor_norm

    def get_psi(self, time_index=0):
        psi = None
        if len(self.ids_object.profiles_1d[time_index].grid.psi) > 0:
            psi = -self.ids_object.profiles_1d[time_index].grid.psi
        return psi

    def get_volume(self, slice_index=0):
        volume = self.ids_object.profiles_1d[slice_index].grid.volume
        if len(volume) == 0:
            volume = None
            print("!   core_profile IDS: Grid volume is empty")
        return volume

    def get_single_species_density(self, slice_index=0, species_index=0):
        """
        Sum of multiplication of volume and species density

        Args:
            slice_index (int, optional): [slice on which functions should operate on]. Defaults to 0.
            species_index (int, optional): [species from which we need to get the data]. Defaults to 0.

        Returns:
            [float]: [Sum of multiplication of volume and elcetrons density ]
        """
        volume = self.volume
        density = self.ids_object.profiles_1d[slice_index].ion[species_index].density
        return sum(volume * density)

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
            species_density_list[ispecies] = self.get_single_species_density(
                slice_index=0, species_index=ispecies
            )
            sum_density = sum_density + species_density_list[ispecies]
            if species_density_list[ispecies] > max_density:
                max_density = species_density_list[ispecies]
                max_density_index = ispecies
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

        a = self.get_a()
        z = self.get_z()
        species = []
        for ispecies in range(nspecies):
            species.append(table_mendeleiev[z[ispecies]][a[ispecies]].element)
        return species

    def get_species_labels(self, slice_index=0) -> list:
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
