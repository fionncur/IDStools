import numpy as np
import database_tools.init_mendeleiev as mend


class CoreProfilesCompute:
    def __init__(self, ids_object, slice_index=0):
        super().__init__()
        self.ids_object = ids_object
        self.slice_index = slice_index

    @staticmethod
    def get_plasma_composition_with_species_concentration(ids_object, slice_index=0):
        coreProfileCompute = CoreProfilesCompute(ids_object, slice_index)

        data = {}

        nspec_over_ntot = coreProfileCompute.get_nspec_over_ntot()
        nspec_over_ne = coreProfileCompute.get_nspec_over_ne()
        nspec_over_nmaj = coreProfileCompute.get_nspec_over_nmaj()
        species = coreProfileCompute.get_species()
        coreProfileCompute.combine_species_when_appear_twice(
            species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj
        )

        data["nspec_over_ntot"] = nspec_over_ntot
        data["nspec_over_ne"] = nspec_over_ne
        data["nspec_over_nmaj"] = nspec_over_nmaj

        data["species"] = species
        data["nspecies"] = len(species)
        data["a"] = coreProfileCompute.get_a()
        data["z"] = coreProfileCompute.get_z()

        data["states_data"] = coreProfileCompute.get_states_data()
        return data

    def get_a(self, slice_index=0, element_index=0):
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

    def get_z(self, slice_index=0, element_index=0):
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

    def get_states(self, slice_index=0):
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)
        states = []
        for species_index in range(nspecies):
            states.append(
                self.ids_object.profiles_1d[slice_index].ion[species_index].state
            )
        return states

    def get_states_data(self, slice_index=0):
        states_data = {}

        volume = self.ids_object.profiles_1d[slice_index].grid.volume
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

                try:
                    states_density[state_index] = sum(
                        (
                            self.ids_object.profiles_1d[slice_index]
                            .ion[species_index]
                            .state[state_index]
                            .density
                            * volume
                        )
                    )
                except:
                    try:
                        states_density[state_index] = sum(
                            self.ids_object.profiles_1d[slice_index]
                            .ion[species_index]
                            .state[state_index]
                            .density_thermal
                            * volume
                        )
                    except:
                        print("!  Error with density data")
                state_data["states_density"] = states_density
                state_data["n_ni"] = (
                    100 * states_density[state_index] / species_density[species_index]
                )
                species_data[str(state_index)] = state_data
            label = self.ids_object.profiles_1d[slice_index].ion[species_index].label
            states_data[label] = species_data
        return states_data

    def get_ne(self, slice_index=0):
        volume = self.ids_object.profiles_1d[slice_index].grid.volume
        electron_density = self.ids_object.profiles_1d[slice_index].electrons.density
        return sum(volume * electron_density)

    def get_single_species_density(self, slice_index=0, species_index=0):
        volume = self.ids_object.profiles_1d[slice_index].grid.volume
        density = self.ids_object.profiles_1d[slice_index].ion[species_index].density
        return sum(volume * density)

    def get_species_density(self, slice_index=0):
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
        species_density_list, sum_density, _ = self.get_species_density()
        return species_density_list / sum_density

    def get_nspec_over_ne(self):
        species_density_list, _, _ = self.get_species_density()
        ne = self.get_ne()
        return species_density_list / ne

    def get_nspec_over_nmaj(self):
        (
            species_density_list,
            _,
            max_density_index,
        ) = self.get_species_density()
        return species_density_list / species_density_list[max_density_index]

    def get_species(self, slice_index=0):
        table_mendeleiev = mend.create_table_mendeleiev()
        nspecies = len(self.ids_object.profiles_1d[slice_index].ion)

        a = self.get_a()
        z = self.get_z()
        species = []
        for ispecies in range(nspecies):
            species.append(table_mendeleiev[z[ispecies]][a[ispecies]].element)
        return species

    def combine_species_when_appear_twice(
        self, species, nspec_over_ntot, nspec_over_ne, nspec_over_nmaj, slice_index=0
    ):
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
