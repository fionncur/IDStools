import logging
import numpy as np
import imas  # noqa: F401
from idstools.compute.common import getNearestTime
from idstools.compute.core_profiles import CoreProfilesCompute
from idstools.compute.edge_profiles import EdgeProfilesCompute
from idstools.compute.equilibrium import EquilibriumCompute

logger = logging.getLogger("module")


class kinetic_profiles_compute:
    i_m_p_u_r_i_t_y__l_i_m_i_t = 0.001

    def __init__(self):
        self.connection = None
        self.edge_required = None

        self.core_profiles = None
        self.edge_profiles = None
        self.equilibrium = None

        self.is_core_profiles_present = True
        self.is_edge_profiles_present = False
        self.is_equilibrium_present = False

        self.r_out_graph = False
        self.common_time_length = None
        self.common_time_array = None

        self.initialised = None

        self.is_composition_available = True
        self.gset = None
        self.nrho = None
        self.mrho = None
        self.erho = None
        self.nspecies_core = None
        self.nspecies_edge = None
        self.ti_flag = None
        self.ti_e_flag = None
        self.species_map = None

        self.xbeg = None
        self.xend = None
        self.rho_tor_norm = None

        self.a = None
        self.z = None
        self.n = None
        self.species_map = None
        self.volume = None
        self.zeff = None
        self.electron_density = None
        self.electron_temperature = None
        self.ti_flag = None
        self.ti_e_flag = None
        self.ion_temperature = None
        self.ion_density = None

        self.vtor_flag = None
        self.vtor_e_flag = None
        self.ion_vtor = None

        self.vpol_flag = None
        self.vpol_e_flag = None
        self.ion_vpol = None

        self.species = None
        self.nspec_over_ne = None

        self.profiles = None

        self.max_vtor = None
        self.min_vtor = None
        self.max_vpol = None
        self.min_vpol = None

        self.waveform = None

    def analyze(self, connection, edge_required=False, time_slice=-99.0):
        self.connection = connection
        self.edge_required = edge_required
        self.initialised = self.check_i_d_ses()
        self.fill_i_d_ses(time_slice)

        self.edge_profiles_compute = EdgeProfilesCompute(self.edge_profiles)
        self.core_profiles_compute = CoreProfilesCompute(self.core_profiles)
        self.equlibrium_compute = EquilibriumCompute(self.equilibrium)

        self.gset = self.getgset()
        (
            self.nrho,
            self.mrho,
            self.erho,
        ) = self.get_rho_tor_norm()
        self.nspecies_core, self.nspecies_edge = self.get_species()

        rho_or_r_outboard_profile = self.get_rho_or_r_outboard_profile()
        self.xbeg = rho_or_r_outboard_profile["xbeg"]
        self.xend = rho_or_r_outboard_profile["xend"]
        self.rho_tor_norm = rho_or_r_outboard_profile["rho_tor_norm"]

        self.nspecies_core, self.nspecies_core_edge = self.get_species()
        self.a = self.get_species_a_number()  # Species A number (not mandatory)
        self.z = self.get_species_z_number()  # Species Z number (not mandatory)
        self.n = self.get_species_atoms_n()  # Number of atoms per species (not mandatory)
        self.species_map = self.get_species_map()
        self.volume = self.get_volume_profile()  # Volume profile (not mandatory)
        self.zeff = self.get_zeff_profile()  # Zeff profile (not mandatory)
        self.electron_density = self.getne_profile()  # Ne profile (not mandatory)
        self.electron_temperature = self.gette_profile()  # Te profile (not mandatory)
        self.ti_flag, self.ti_e_flag = self.getti_flag()  # Ti profile (not mandatory)
        self.ion_temperature = self.get_ion_temperature()  # ion temerature
        self.ion_density = self.get_ion_density()  # Ni profile (not mandatory)
        vtor_profile = self.get_v_tor_profile()  # Vtor profile (not mandatory)
        self.vtor_flag = vtor_profile["vtor_flag"]
        self.vtor_e_flag = vtor_profile["vtor_e_flag"]
        self.ion_vtor = vtor_profile["ion_vtor"]
        vpol_profile = self.get_vpol_profile()  # Vpol profile (not mandatory)
        self.vpol_flag = vpol_profile["vpol_flag"]
        self.vpol_e_flag = vpol_profile["vpol_e_flag"]
        self.ion_vpol = vpol_profile["ion_vpol"]
        self.species = self.get_species_list()
        self.nspec_over_ne = self.get_n_spec_nver_ne()

        self.profiles = self.get_profiles()  # Create the dictionary defining the list of profiles

        velocity_profiles = self.get_min_max_velocity_profiles()  # Min and max of velocity profiles
        self.max_vtor = velocity_profiles["max_vtor"]
        self.min_vtor = velocity_profiles["min_vtor"]
        self.max_vpol = velocity_profiles["max_vpol"]
        self.min_vpol = velocity_profiles["min_vpol"]

        self.waveform = self.get_waveform()  # Create the dictionary defining the list of waveforms (central values)

    def get_i_d_s(self, ids_name=""):
        ids_present = False
        ids_object = None
        if ids_name:
            try:
                ids_object = eval(f"imas.{ids_name}()")  # To initialise the empty IDS structure
                ids_object.time = self.connection.partial_get(ids_name, "time")
                if ids_object.time is not None:
                    if len(ids_object.time) > 0:
                        ids_present = True
                else:
                    logger.critical(f"No {ids_name} IDS in the data-entry.")
                    ids_present = False
            except Exception as e:
                logger.debug(f"{e}")
                logger.critical(f"The {ids_name} IDS is absent from the input data-entry.")
                ids_present = False
        return ids_object, ids_present

    def check_i_d_ses(self):
        self.core_profiles, self.is_core_profiles_present = self.get_i_d_s("core_profiles")
        if self.edge_required:
            self.edge_profiles, self.is_edge_profiles_present = self.get_i_d_s("edge_profiles")
            if self.is_core_profiles_present:
                logger.info("Found adjoining edge_profiles. Will attempt to add to plots.")
            else:
                logger.info("Found edge_profiles IDS in data-entry. Will only plot edge data.")
        self.equilibrium, self.is_equilibrium_present = self.get_i_d_s("equilibrium")

        if not self.is_core_profiles_present and not self.is_edge_profiles_present:
            logger.critical("No data found to plot. --> Abort.")
            logger.critical("----> Aborted.")
            return None
        return True

    def fill_i_d_ses(self, time_slice=-99.0):
        # Search for adequate time slice for display
        if self.is_core_profiles_present:
            self.common_time_length = len(self.core_profiles.time)
            self.common_time_array = self.core_profiles.time
        else:
            self.common_time_length = len(self.edge_profiles.time)
            self.common_time_array = self.edge_profiles.time
        self.common_time = time_slice
        common_time_index, common_time_value = get_nearest_time(self.common_time_array, time_slice)

        self.common_time = common_time_value

        # Read 1D-profiles for this time slice
        if self.is_core_profiles_present:
            self.core_profiles.profiles_1d.resize(1)
            self.core_profiles.profiles_1d[0] = self.connection.partial_get(
                "core_profiles", f"profiles_1d({common_time_index})"
            )

        # Read equilibrium data for this time slice if present
        if self.is_equilibrium_present:
            # ntimeEquilibrium = len(self.equilibrium.time)
            time_array_equilibrium = self.equilibrium.time
            time_index_equilibrium, time_value_equilibrium = get_nearest_time(time_array_equilibrium, self.common_time)

        # Add 1D-profiles edge data if present

        if self.is_edge_profiles_present:
            # ntimeEdgeProfiles = len(self.edge_profiles.time)
            time_array_edge_profiles = self.edge_profiles.time
            time_index_edge_profiles, time_value_edge_profiles = get_nearest_time(
                time_array_edge_profiles, self.common_time
            )

            # Read edge_profile data for this time slice
            try:
                self.edge_profiles.profiles_1d.resize(1)
                self.edge_profiles.profiles_1d[0] = self.connection.partial_get(
                    "edge_profiles", f"profiles_1d({time_index_edge_profiles})"
                )
                # teme = timeValueEdgeProfiles
            except Exception as e:
                logger.debug(f"{e}")
                logger.warning("No profiles_1d information found in edge_profiles IDS.")
                if self.is_equilibrium_present and len(self.equilibrium.time) > 0:
                    self.equilibrium.time_slice.resize(1)
                    self.equilibrium.time_slice[0] = self.connection.partial_get(
                        "equilibrium", f"time_slice({time_index_equilibrium})"
                    )
                    # tqme = timeValueEquilibrium
                    if (
                        len(self.equilibrium.time_slice[0].profiles_1d.r_outboard) > 0
                        or not self.is_core_profiles_present
                    ):
                        self.edge_profiles.grid_ggd.resize(1)
                        try:
                            self.edge_profiles.grid_ggd[0] = self.connection.partial_get(
                                "edge_profiles",
                                f"grid_ggd({time_index_edge_profiles})",
                            )
                        except Exception as e:
                            logger.debug(f"{e}")
                            self.is_edge_profiles_present = False
                            logger.warning("No grid_ggd information found in edge_profiles IDS.")
                        self.edge_profiles.ggd.resize(1)
                        try:
                            self.edge_profiles.ggd[0] = self.connection.partial_get(
                                "edge_profiles", f"ggd({time_index_edge_profiles})"
                            )
                        except Exception as e:
                            logger.debug(f"{e}")
                            self.is_edge_profiles_present = False
                            logger.warning("No ggd information found in edge_profiles IDS.")
                        if self.is_edge_profiles_present:
                            self.r_out_graph = True
                            logger.info("Attempting to use R_outboard coordinate instead.")
                    else:
                        if self.is_core_profiles_present:
                            self.is_edge_profiles_present = False
                else:
                    if self.is_core_profiles_present:
                        self.is_edge_profiles_present = False
                    else:
                        self.edge_profiles.grid_ggd.resize(1)
                        try:
                            self.edge_profiles.grid_ggd[0] = self.connection.partial_get(
                                "edge_profiles",
                                f"grid_ggd({time_index_edge_profiles})",
                            )
                        except Exception as e:
                            logger.debug(f"{e}")
                            self.is_edge_profiles_present = False
                            logger.warning("No grid_ggd information found in edge_profiles IDS.")
                        self.edge_profiles.ggd.resize(1)
                        try:
                            self.edge_profiles.ggd[0] = self.connection.partial_get(
                                "edge_profiles", f"ggd({time_index_edge_profiles})"
                            )
                        except Exception as e:
                            logger.debug(f"{e}")
                            self.is_edge_profiles_present = False
                            logger.warning("No ggd information found in edge_profiles IDS.")
                        if self.is_edge_profiles_present:
                            self.r_out_graph = True
                            logger.info("Attempting to use R coordinate instead.")

    def getgset(self):
        if self.r_out_graph:
            gset = self.edge_profiles_compute.get_outer_midplane_array_index()
            if gset is None:
                logger.warning("Abandoning edge plots !")
                self.is_edge_profiles_present = False
                self.r_out_graph = False
            try:
                if self.edge_profiles.midplane.index != 1 and self.r_out_graph and self.is_core_profiles_present:
                    logger.warning("Edge and core profile midplane coordinates are not aligned!")
            except Exception as e:
                logger.debug(f"{e}")
                logger.warning("Edge_profiles midplane location not specified! Coordinates may be misaligned.")
            return gset
        return None

    def get_rho_or_r_outboard_profile(self):
        xbeg = 99.0
        xend = 0
        rho_tor_norm = [0] * (self.nrho + self.erho)
        if not self.r_out_graph and self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].grid.rho_tor_norm) > 0:
                for i in range(self.nrho):
                    rho_tor_norm[i] = self.core_profiles.profiles_1d[0].grid.rho_tor_norm[i]
            elif len(self.core_profiles.profiles_1d[0].grid.rho_tor) > 0:
                for i in range(self.nrho):
                    rho_tor_norm[i] = (
                        self.core_profiles.profiles_1d[0].grid.rho_tor[i]
                        / self.core_profiles.profiles_1d[0].grid.rho_tor[self.nrho - 1]
                    )
            xbeg = 0
            xend = 1
        elif self.is_core_profiles_present:
            for i in range(self.nrho):
                rho_tor_norm[i] = self.equilibrium.time_slice[0].profiles_1d.r_outboard[self.mrho + i]
            xbeg = min(xbeg, rho_tor_norm[self.nrho - 1], rho_tor_norm[0])
            xend = max(xend, rho_tor_norm[self.nrho - 1], rho_tor_norm[0])

        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                if len(self.core_profiles.profiles_1d[0].grid.rho_tor_norm) > 0:
                    for i in range(self.erho):
                        rho_tor_norm[self.nrho + i] = self.edge_profiles.profiles_1d[0].rho_tor_norm[i]
                elif len(self.core_profiles.profiles_1d[0].grid.rho_tor) > 0:
                    for i in range(self.erho):
                        rho_tor_norm[self.nrho + i] = (
                            self.edge_profiles.profiles_1d[0].grid.rho_tor[i]
                            / self.core_profiles.profiles_1d[0].grid.rho_tor[self.nrho - 1]
                        )
                xbeg = min(xbeg, rho_tor_norm[self.nrho + self.erho - 1], rho_tor_norm[0])
                xend = max(
                    xend,
                    rho_tor_norm[self.nrho + self.erho - 1],
                    rho_tor_norm[self.nrho],
                )
            else:
                if self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension == -999999999:
                    logger.debug("Dimensionality of Outer Midplane GGD subset is not defined !")
                    logger.debug("Assuming the grid subset is made of edges (dimensionality 2).")
                if self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension == 1:
                    for i in range(self.erho):
                        ielem = self.edge_profiles.grid_ggd[0].grid_subset[self.gset].element[i].object[0].index
                        i1 = self.edge_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[ielem - 1].nodes[0]
                        rho_tor_norm[self.nrho + i] = (
                            self.edge_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[i1 - 1].geometry[0]
                        )
                        xbeg = min(xbeg, rho_tor_norm[0])
                        xend = max(xend, rho_tor_norm[self.nrho + i])
                elif (
                    self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension == 2
                    or self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension == -999999999
                ) and self.is_edge_profiles_present:
                    for i in range(self.erho):
                        ielem = self.edge_profiles.grid_ggd[0].grid_subset[self.gset].element[i].object[0].index
                        i1 = self.edge_profiles.grid_ggd[0].space[0].objects_per_dimension[1].object[ielem - 1].nodes[0]
                        i2 = self.edge_profiles.grid_ggd[0].space[0].objects_per_dimension[1].object[ielem - 1].nodes[1]
                        rho_tor_norm[self.nrho + i] = (
                            self.edge_profiles.grid_ggd[0].space[0].objects_per_dimension[0].object[i1 - 1].geometry[0]
                            + self.edge_profiles.grid_ggd[0]
                            .space[0]
                            .objects_per_dimension[0]
                            .object[i2 - 1]
                            .geometry[0]
                        ) / 2
                        xbeg = min(xbeg, rho_tor_norm[0])
                        xend = max(xend, rho_tor_norm[self.nrho + i])
                else:
                    logger.warning(
                        f"Unexpected dimensionality of Outer Midplane GGD subset :"
                        f"{self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension}"
                    )
                    logger.warning("Abandoning edge plots !")
                    self.is_edge_profiles_present = False
        return {"xbeg": xbeg, "xend": xend, "rho_tor_norm": rho_tor_norm}

    def get_species(self):
        nspecies_core = 0
        if self.is_core_profiles_present:
            try:
                nspecies_core = len(self.core_profiles.profiles_1d[0].ion)
            except Exception as e:
                logger.debug(f"{e}")
                logger.critical("core_profiles.profiles_1d[0].ion could not be read.")
                return None

        nspecies_edge = nspecies_core
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                nspecies_edge = len(self.edge_profiles.profiles_1d[0].ion)
            else:
                nspecies_edge = len(self.edge_profiles.ggd[0].ion)
        if nspecies_core != nspecies_edge and self.is_core_profiles_present and self.is_edge_profiles_present:
            logger.warning("Warning: list of species in core and edge profiles data do not match!")
        if not self.is_core_profiles_present:
            nspecies_core = nspecies_edge

        return nspecies_core, nspecies_edge

    def get_species_a_number(self):
        a = [0] * self.nspecies_core
        if self.is_core_profiles_present:
            try:
                for ispecies in range(self.nspecies_core):
                    a[ispecies] = int(self.core_profiles.profiles_1d[0].ion[ispecies].element[0].a)
            except Exception as e:
                logger.debug(f"{e}")
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].a could not be read.")
                self.is_composition_available = False  # plot_compo
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspecies_core_edge):
                        a[ispecies] = int(self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].a)
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].a could not be read.")
                    self.is_composition_available = False
            else:
                try:
                    for ispecies in range(self.nspecies_core_edge):
                        a[ispecies] = int(self.edge_profiles.ggd[0].ion[ispecies].element[0].a)
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].a could not be read.")
                    self.is_composition_available = False
        return a

    def get_species_z_number(self):
        z = [0] * self.nspecies_core
        if self.is_core_profiles_present:
            try:
                for ispecies in range(self.nspecies_core):
                    z[ispecies] = int(self.core_profiles.profiles_1d[0].ion[ispecies].element[0].z_n)
            except Exception as e:
                logger.debug(f"{e}")
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].z_n could not be read.")
                self.is_composition_available = False
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspecies_edge):
                        z[ispecies] = int(self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].z_n)
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].z_n could not be read.")
                    self.is_composition_available = False
            else:
                try:
                    for ispecies in range(self.nspecies_edge):
                        z[ispecies] = int(self.edge_profiles.ggd[0].ion[ispecies].element[0].z_n)
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].z_n could not be read.")
                    self.is_composition_available = False
        return z

    def get_species_atoms_n(self):
        n = [1] * self.nspecies_core
        if self.is_core_profiles_present:
            try:
                for ispecies in range(self.nspecies_core):
                    n[ispecies] = self.core_profiles.profiles_1d[0].ion[ispecies].element[0].atoms_n
            except Exception as e:
                logger.debug(f"{e}")
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].atoms_n could not be read.")
                logger.warning("Value of 1 assumed.")
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspecies_edge):
                        n[ispecies] = self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].atoms_n
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].atoms_n could not be read.")
                    logger.warning("Value of 1 assumed.")
            else:
                try:
                    for ispecies in range(self.nspecies_edge):
                        n[ispecies] = self.edge_profiles.ggd[0].ion[ispecies].element[0].atoms_n
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].atoms_n could not be read.")
                    logger.warning("Value of 1 assumed.")
        return n

    def get_species_map(self):
        if self.is_edge_profiles_present:
            species_map = [-99] * self.nspecies_core
            for ispecies in range(self.nspecies_core):
                for jspecies in range(self.nspecies_edge):
                    if self.r_out_graph == 0:
                        if (
                            self.a[ispecies] == int(self.edge_profiles.profiles_1d[0].ion[jspecies].element[0].a)
                            and self.z[ispecies] == int(self.edge_profiles.profiles_1d[0].ion[jspecies].element[0].z_n)
                            and self.n[ispecies] == self.edge_profiles_1d[0].ion[jspecies].element[0].atoms_n
                        ):
                            species_map[ispecies] = jspecies
                    else:
                        if (
                            self.a[ispecies] == int(self.edge_profiles.ggd[0].ion[jspecies].element[0].a)
                            and self.z[ispecies] == int(self.edge_profiles.ggd[0].ion[jspecies].element[0].z_n)
                            and self.n[ispecies] == self.edge_profiles.ggd[0].ion[jspecies].element[0].atoms_n
                        ):
                            species_map[ispecies] = jspecies
                if species_map[ispecies] == -99 and self.is_core_profiles_present == 1:
                    logger.warning(
                        "Core_profiles species "
                        + self.core_profiles.profiles_1d[0].ion[ispecies].label
                        + " has no partner in edge_profiles!"
                    )
            self.species_map = species_map
            return species_map
        return None

    def get_rho_tor_norm(self):
        nrho = 0
        mrho = 0
        if not self.r_out_graph and self.is_core_profiles_present:
            nrho = self.core_profiles_compute.getnrho()
            if nrho is None or nrho == 0:
                logger.error("core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty.")
                logger.error("----> Aborted.")
                exit()
        else:
            if self.is_core_profiles_present:
                if len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm) == len(
                    self.core_profiles.profiles_1d[0].grid.rho_tor_norm
                ):
                    nrho = len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm)
                else:
                    mrho = self.equlibrium_compute.getmrho()
                    nrho = len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm) - mrho

        erho = 0
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                erho = self.core_profiles_compute.getnrho()
                if nrho is None or nrho == 0:
                    logger.warning("edge_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty.")
            else:
                erho = len(self.edge_profiles.grid_ggd[0].grid_subset[self.gset].element)
        return nrho, mrho, erho

    def get_volume_profile(self):
        volume = [0] * (self.nrho + self.erho)
        if self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].grid.volume) == self.nrho:
                for i in range(self.nrho):
                    volume[i] = self.core_profiles.profiles_1d[0].grid.volume[i]
            else:
                try:
                    equilibrium = self.connection.equilibrium
                    equilibrium.time_slice[0].profiles_1d.volume = self.connection.partial_get(
                        "equilibrium",
                        f"time_slice({self.common_time_index})/profiles_1d/volume",
                    )
                    for i in range(self.nrho):
                        volume[i] = equilibrium.time_slice[0].profiles_1d.volume[i]
                    if len(volume) == len(self.core_profiles.profiles_1d[0].electrons.density):
                        logger.warning("   core_profiles.profiles_1d[:].grid.volume could not be read.")
                        logger.warning("   ----> equilibrium.time_slice[:].profiles_1d.volume used instead.")
                        logger.warning("   (possible because the resolution is the same, but maybe not correct)")
                except Exception as e:
                    logger.debug(f"{e}")
                    logger.warning("core_profiles.profiles_1d[:].grid.volume could not be read.")
                    self.is_composition_available = False
        if self.is_edge_profiles_present and not self.r_out_graph:
            for i in range(self.erho):
                volume[self.nrho + i] = self.edge_profiles.profiles_1d[0].grid.volume[i]
        return volume

    def get_zeff_profile(self):
        zeff = [0] * (self.nrho + self.erho)
        if self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].zeff) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].zeff could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, zeff = {len(self.core_profiles.profiles_1d[0].zeff)}"
                )
                self.core_profiles.profiles_1d[0].zeff = np.asarray([np.na_n] * self.nrho)
            for i in range(self.nrho):
                zeff[i] = self.core_profiles.profiles_1d[0].zeff[i]
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].zeff) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].zeff could not be read.")
                    self.edge_profiles.profiles_1d[0].zeff = np.asarray([np.na_n] * self.erho)
                for i in range(self.erho):
                    zeff[self.nrho + i] = self.edge_profiles.profiles_1d[0].zeff[i]
            else:
                if len(self.edge_profiles.ggd[0].zeff[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].zeff could not be read.")
                    self.edge_profiles.ggd[0].zeff[self.gset].values = np.asarray([np.na_n] * self.erho)
                for i in range(self.erho):
                    zeff[self.nrho + i] = self.edge_profiles.ggd[0].zeff[self.gset].values[i]
        return zeff

    def getne_profile(self):
        electron_density = [0] * (self.nrho + self.erho)
        if self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].electrons.density) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].electrons.density could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, electrons.density ="
                    f"{len(self.core_profiles.profiles_1d[0].electrons.density)}"
                )
                self.core_profiles.profiles_1d[0].electrons.density = np.asarray([np.na_n] * self.nrho)
            for i in range(self.nrho):
                electron_density[i] = self.core_profiles.profiles_1d[0].electrons.density[i]
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].electrons.density) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].electrons.density could not be read.")
                    self.edge_profiles.profiles_1d[0].electrons.density = np.asarray([np.na_n] * self.erho)
                for i in range(self.erho):
                    electron_density[self.nrho + i] = self.edge_profiles.profiles_1d[0].electrons.density[i]
            else:
                if len(self.edge_profiles.ggd[0].electrons.density[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].electrons.density could not be read.")
                    self.edge_profiles.ggd[0].electrons.density[self.gset].values = np.asarray([np.na_n] * self.erho)
                for i in range(self.erho):
                    electron_density[self.nrho + i] = self.edge_profiles.ggd[0].electrons.density[self.gset].values[i]
        return electron_density

    def gette_profile(self):
        electron_temperature = [0] * (self.nrho + self.erho)
        if self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].electrons.temperature) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].electrons.temperature could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, electrons.temperature = "
                    f"{len(self.core_profiles.profiles_1d[0].electrons.temperature)}"
                )
                self.core_profiles.profiles_1d[0].electrons.temperature = np.asarray([np.na_n] * self.nrho)
            for i in range(self.nrho):
                electron_temperature[i] = self.core_profiles.profiles_1d[0].electrons.temperature[i] * 1.0e-3
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].electrons.temperature) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].electrons.temperature could not be read.")
                    self.edge_profiles.profiles_1d[0].electrons.temperature = np.asarray([np.na_n] * self.erho)
                for i in range(self.erho):
                    electron_temperature[self.nrho + i] = (
                        self.edge_profiles.profiles_1d[0].electrons.temperature[i] * 1.0e-3
                    )
            else:
                if len(self.edge_profiles.ggd[0].electrons.temperature[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].electrons.temperature could not be read.")
                    self.edge_profiles.ggd[0].electrons.temperature[self.gset].values = np.asarray(
                        [np.na_n] * self.erho
                    )
                for i in range(self.erho):
                    electron_temperature[self.nrho + i] = (
                        self.edge_profiles.ggd[0].electrons.temperature[self.gset].values[i] * 1.0e-3
                    )
        return electron_temperature

    def getti_flag(self):
        ti_flag = 0
        if self.is_core_profiles_present:
            if len(self.core_profiles.profiles_1d[0].t_i_average) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].t_i_average could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, t_i_average = "
                    f"{len(self.core_profiles.profiles_1d[0].t_i_average)}"
                )
                self.core_profiles.profiles_1d[0].t_i_average = np.asarray([np.na_n] * self.nrho)
            else:
                ti_flag = 1
        ti_e_flag = 0
        if self.is_edge_profiles_present:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].t_i_average) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].t_i_average could not be read.")
                    self.edge_profiles.profiles_1d[0].t_i_average = np.asarray([np.na_n] * self.erho)
                else:
                    ti_e_flag = 1
            else:
                if len(self.edge_profiles.ggd[0].t_i_average[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].t_i_average could not be read.")
                    self.edge_profiles.ggd[0].t_i_average[self.gset].values = np.asarray([np.na_n] * self.erho)
                else:
                    ti_e_flag = 1

        if ti_flag == 0:
            for ispecies in range(self.nspecies_core):
                if self.is_core_profiles_present:
                    if len(self.core_profiles.profiles_1d[0].ion[ispecies].temperature) != self.nrho:
                        logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].temperature could not be read.")
                        logger.warning(
                            f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].temperature = "
                            f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].temperature)}"
                        )
                        self.core_profiles.profiles_1d[0].ion[ispecies].temperature = np.asarray([np.na_n] * self.nrho)
                    else:
                        ti_flag = 2
                if self.is_edge_profiles_present and ti_e_flag == 0:
                    jspecies = self.species_map[ispecies]
                    if jspecies != -99:
                        if not self.r_out_graph:
                            if len(self.edge_profiles.profiles_1d[0].ion[jspecies].temperature) < 1:
                                if ti_e_flag != 1:
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].temperature could not be read."
                                    )
                                    self.edge_profiles.profiles_1d[0].ion[jspecies].temperature = np.asarray(
                                        [np.na_n] * self.erho
                                    )
                            else:
                                ti_e_flag = 2
                        else:
                            if len(self.edge_profiles.ggd[0].ion[jspecies].temperature) < 1:
                                if ti_e_flag != 1:
                                    logger.warning("edge_profiles.ggd[:].ion[:].temperature could not be read.")
                                    self.edge_profiles.ggd[0].ion[jspecies].temperature[self.gset].values = np.asarray(
                                        [np.na_n] * self.erho
                                    )
                            else:
                                ti_e_flag = 2

        logger.info(f"Ti_flag : {ti_flag}, Ti_e_flag : {ti_e_flag}")
        self.ti_flag = ti_flag
        self.ti_e_flag = ti_e_flag
        return ti_flag, ti_e_flag

    def get_ion_temperature(self):
        ion_temperature = [0] * (self.nrho + self.erho)
        if self.ti_flag == 1:
            for i in range(self.nrho):
                ion_temperature[i] = self.core_profiles.profiles_1d[0].t_i_average[i] * 1.0e-3
        elif self.ti_flag == 2:
            for i in range(self.nrho):
                ion_temperature[i] = self.core_profiles.profiles_1d[0].ion[0].temperature[i] * 1.0e-3
        if self.is_edge_profiles_present:
            if self.ti_e_flag == 1:
                if not self.r_out_graph:
                    for i in range(self.erho):
                        ion_temperature[self.nrho + i] = self.edge_profiles.profiles_1d[0].t_i_average[i] * 1.0e-3
                else:
                    for i in range(self.erho):
                        ion_temperature[self.nrho + i] = (
                            self.edge_profiles.ggd[0].t_i_average[self.gset].values[i] * 1.0e-3
                        )
            elif self.ti_e_flag == 2:
                if not self.r_out_graph:
                    for i in range(self.erho):
                        ion_temperature[self.nrho + i] = (
                            self.edge_profiles.profiles_1d[0].ion[0].temperature[i] * 1.0e-3
                        )
                else:
                    for i in range(self.erho):
                        ion_temperature[self.nrho + i] = (
                            self.edge_profiles.ggd[0].ion[0].temperature[self.gset].values[i] * 1.0e-3
                        )
        return ion_temperature

    def get_ion_density(self):
        ion_density = {}
        for ispecies in range(self.nspecies_core):
            ion_density[ispecies] = [0] * (self.nrho + self.erho)
            if self.is_core_profiles_present:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].density) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].density could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].density = "
                        f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].density)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].density = np.asarray([np.na_n] * self.nrho)
                for i in range(self.nrho):
                    ion_density[ispecies][i] = self.core_profiles.profiles_1d[0].ion[ispecies].density[i]
            if self.is_edge_profiles_present:
                jspecies = self.species_map[ispecies]
                if jspecies != -99:
                    if not self.r_out_graph:
                        if self.edge_profiles.profiles_1d[0].ion[jspecies].multiple_states_flag == 0:
                            if len(self.edge_profiles.profiles_1d[0].ion[jspecies].density) < 1:
                                logger.warning(
                                    f"edge_profiles.profiles_1d[:].ion[{jspecies}].density could not be read."
                                )
                                self.edge_profiles.profiles_1d[0].ion[jspecies].density = np.asarray(
                                    [np.na_n] * self.erho
                                )
                            for i in range(self.erho):
                                ion_density[ispecies][self.nrho + i] = (
                                    self.edge_profiles.profiles_1d[0].ion[jspecies].density[i]
                                )
                        else:
                            for istate in range(len(self.edge_profiles.profiles_1d[0].ion[jspecies].state)):
                                if len(self.edge_profiles.profiles_1d[0].ion[jspecies].state[istate].density) < 1:
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}].density "
                                        f"could not be read."
                                    )
                                    self.edge_profiles.profiles_1d[0].ion[jspecies].state[istate].density = np.asarray(
                                        [0] * self.erho
                                    )
                                for i in range(self.erho):
                                    ion_density[ispecies][self.nrho + i] = (
                                        ion_density[ispecies][self.nrho + i]
                                        + self.edge_profiles.profiles_1d[0].ion[jspecies].state[istate].density[i]
                                    )
                    else:
                        if self.edge_profiles.ggd[0].ion[jspecies].multiple_states_flag == 0:
                            if len(self.edge_profiles.ggd[0].ion[jspecies].density[self.gset].values) < 1:
                                logger.warning(f"edge_profiles.ggd[:].ion[{jspecies}.density could not be read.")
                                self.edge_profiles.ggd[0].ion[jspecies].density[self.gset].values = np.asarray(
                                    [np.na_n] * self.erho
                                )
                            for i in range(self.erho):
                                ion_density[ispecies][self.nrho + i] = (
                                    self.edge_profiles.ggd[0].ion[jspecies].density[self.gset].values[i]
                                )
                        else:
                            for istate in range(len(self.edge_profiles.ggd[0].ion[jspecies].state)):
                                if len(self.edge_profiles.ggd[0].ion[jspecies].state[istate].density) < 1:
                                    logger.warning(
                                        f"edge_profiles.ggd[:].ion[{jspecies}].state[{istate}].density "
                                        f"could not be read."
                                    )
                                    self.edge_profiles.ggd[0].ion[jspecies].state[istate].density = np.asarray(
                                        [0] * self.erho
                                    )
                                for i in range(self.erho):
                                    ion_density[ispecies][self.nrho + i] = (
                                        ion_density[ispecies][self.nrho + i]
                                        + self.edge_profiles.ggd[0]
                                        .ion[jspecies]
                                        .state[istate]
                                        .density[self.gset]
                                        .values[i]
                                    )
        return ion_density

    def get_v_tor_profile(self):
        vtor_flag = 0
        vtor_e_flag = 0
        ion_vtor = {}
        for ispecies in range(self.nspecies_core):
            ion_vtor[ispecies] = [0] * (self.nrho + self.erho)
            if self.is_core_profiles_present:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity.toroidal could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity.toroidal = "
                        f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal = np.asarray(
                        [np.na_n] * self.nrho
                    )
                else:
                    vtor_flag = 1
                    for i in range(self.nrho):
                        ion_vtor[ispecies][i] = abs(
                            self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal[i]
                        )
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity_tor could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity_tor = "
                        f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor = np.asarray([np.na_n] * self.nrho)
                else:
                    if vtor_flag == 0:
                        vtor_flag = 2
                        for i in range(self.nrho):
                            ion_vtor[ispecies][i] = abs(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor[i])
            if self.is_edge_profiles_present:
                jspecies = self.species_map[ispecies]
                if jspecies != -99:
                    if not self.r_out_graph:
                        if self.edge_profiles.profiles_1d[0].ion[jspecies].multiple_states_flag == 0:
                            try:
                                if len(self.edge_profiles.profiles_1d[0].ion[jspecies].velocity.toroidal) == self.erho:
                                    for i in range(self.erho):
                                        ion_vtor[ispecies][self.nrho + i] = abs(
                                            self.edge_profiles.profiles_1d[0].ion[jspecies].velocity.toroidal[i]
                                        )
                                    vtor_e_flag = 1
                            except Exception as e:
                                logger.debug(f"{e}")
                                logger.warning(
                                    f"edge_profiles.profiles_1d[:].ion[{jspecies}].velocity.toroidal could not be read."
                                )
                            if vtor_e_flag != 1:
                                try:
                                    if len(self.edge_profiles.profiles_1d[0].ion[jspecies].velocity_tor) == self.erho:
                                        for i in range(self.erho):
                                            ion_vtor[ispecies][self.nrho + i] = abs(
                                                self.edge_profiles.profiles_1d[0].ion[jspecies].velocity_tor[i]
                                            )
                                        vtor_e_flag = 2
                                except Exception as e:
                                    logger.debug(f"{e}")
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].velocity_tor could not be read."
                                    )
                        else:
                            for istate in range(len(self.edge_profiles.profiles_1d[0].ion[jspecies].state)):
                                try:
                                    if (
                                        len(
                                            self.edge_profiles.profiles_1d[0]
                                            .ion[jspecies]
                                            .state[istate]
                                            .velocity.toroidal
                                        )
                                        == self.erho
                                    ):
                                        for i in range(self.erho):
                                            if self.ion_density[ispecies][self.nrho + i] > 0.0:
                                                ion_vtor[ispecies][self.nrho + i] = (
                                                    ion_vtor[ispecies][self.nrho + i]
                                                    + abs(
                                                        self.edge_profiles.profiles_1d[0]
                                                        .ion[jspecies]
                                                        .state[istate]
                                                        .velocity.toroidal[i]
                                                    )
                                                    * self.edge_profiles.profiles_1d[0]
                                                    .ion[jspecies]
                                                    .state[istate]
                                                    .density[i]
                                                    / self.ion_density[ispecies][self.nrho + i]
                                                )
                                        vtor_e_flag = 1
                                except Exception as e:
                                    logger.debug(f"{e}")
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}]."
                                        f"velocity.toroidal could not be read."
                                    )
                                if vtor_e_flag != 1:
                                    try:
                                        if (
                                            len(
                                                self.edge_profiles.profiles_1d[0]
                                                .ion[jspecies]
                                                .state[istate]
                                                .velocity_tor
                                            )
                                            == self.erho
                                        ):
                                            for i in range(self.erho):
                                                if self.ion_density[ispecies][self.nrho + i] > 0.0:
                                                    ion_vtor[ispecies][self.nrho + i] = (
                                                        ion_vtor[ispecies][self.nrho + i]
                                                        + abs(
                                                            self.edge_profiles.profiles_1d[0]
                                                            .ion[jspecies]
                                                            .state[istate]
                                                            .velocity_tor[i]
                                                        )
                                                        * self.edge_profiles.profiles_1d[0]
                                                        .ion[jspecies]
                                                        .state[istate]
                                                        .density[i]
                                                        / self.ion_density[ispecies][self.nrho + i]
                                                    )
                                            vtor_e_flag = 2
                                    except Exception as e:
                                        logger.debug(f"{e}")
                                        logger.warning(
                                            f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}]."
                                            f"velocity_tor could not be read."
                                        )

                    else:
                        if self.edge_profiles.ggd[0].ion[jspecies].multiple_states_flag == 0:
                            try:
                                if (
                                    len(self.edge_profiles.ggd[0].ion[jspecies].velocity[self.gset].toroidal)
                                    == self.erho
                                ):
                                    for i in range(self.erho):
                                        ion_vtor[ispecies][self.nrho + i] = abs(
                                            self.edge_profiles.ggd[0].ion[jspecies].velocity[self.gset].toroidal[i]
                                        )
                                    vtor_e_flag = 1
                            except Exception as e:
                                logger.debug(f"{e}")
                                logger.warning(
                                    f"edge_profiles.ggd[:].ion[{jspecies}].velocity.toroidal could not be read."
                                )
                        else:
                            for istate in range(len(self.edge_profiles.ggd[0].ion[jspecies].state)):
                                try:
                                    if (
                                        len(
                                            self.edge_profiles.ggd[0]
                                            .ion[jspecies]
                                            .state[istate]
                                            .velocity[self.gset]
                                            .toroidal
                                        )
                                        == self.erho
                                    ):
                                        for i in range(self.erho):
                                            if self.ion_density[ispecies][self.nrho + i] > 0:
                                                ion_vtor[ispecies][self.nrho + i] = (
                                                    ion_vtor[ispecies][self.nrho + i]
                                                    + abs(
                                                        self.edge_profiles.ggd[0]
                                                        .ion[jspecies]
                                                        .state[istate]
                                                        .velocity[self.gset]
                                                        .toroidal[i]
                                                    )
                                                    * self.edge_profiles.ggd[0]
                                                    .ion[jspecies]
                                                    .state[istate]
                                                    .density[self.gset]
                                                    .values[i]
                                                    / self.ion_density[ispecies][self.nrho + i]
                                                )
                                        vtor_e_flag = 1
                                except Exception as e:
                                    logger.debug(f"{e}")
                                    logger.warning(
                                        f"edge_profiles.ggd[:].ion[{jspecies}].state[{istate}]."
                                        f"velocity.toroidal could not be read."
                                    )

        logger.debug(f"Vtor_flag : {vtor_flag}, Vtor_e_flag : {vtor_e_flag}")
        return {
            "vtor_flag": vtor_flag,
            "vtor_e_flag": vtor_e_flag,
            "ion_vtor": ion_vtor,
        }

    def get_vpol_profile(self):
        vpol_flag = 0
        vpol_e_flag = 0
        ion_vpol = {}
        for ispecies in range(self.nspecies_core):
            ion_vpol[ispecies] = [0] * (self.nrho + self.erho)
            if self.is_core_profiles_present:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity.poloidal could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity.poloidal ="
                        f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal = np.asarray(
                        [np.na_n] * self.nrho
                    )
                else:
                    vpol_flag = 1
                    for i in range(self.nrho):
                        ion_vpol[ispecies][i] = abs(
                            self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal[i]
                        )
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity_pol could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity_pol = "
                        f"{len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol = np.asarray([np.na_n] * self.nrho)
                else:
                    if vpol_flag == 0:
                        vpol_flag = 2
                        for i in range(self.nrho):
                            ion_vpol[ispecies][i] = abs(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol[i])
            if self.is_edge_profiles_present:
                jspecies = self.species_map[ispecies]
                if jspecies != -99:
                    if not self.r_out_graph:
                        if self.edge_profiles.profiles_1d[0].ion[jspecies].multiple_states_flag == 0:
                            try:
                                if len(self.edge_profiles.profiles_1d[0].ion[jspecies].velocity.poloidal) == self.erho:
                                    for i in range(self.erho):
                                        ion_vpol[ispecies][self.nrho + i] = abs(
                                            self.edge_profiles.profiles_1d[0].ion[jspecies].velocity.poloidal[i]
                                        )
                                    vpol_e_flag = 1
                            except Exception as e:
                                logger.debug(f"{e}")
                                logger.warning(
                                    f"edge_profiles.profiles_1d[:].ion[{jspecies}].velocity.poloidal could not be read."
                                )
                        else:
                            for istate in range(len(self.edge_profiles.profiles_1d[0].ion[jspecies].state)):
                                try:
                                    if (
                                        len(
                                            self.edge_profiles.profiles_1d[0]
                                            .ion[jspecies]
                                            .state[istate]
                                            .velocity.poloidal
                                        )
                                        == self.erho
                                    ):
                                        for i in range(self.erho):
                                            if self.ion_density[ispecies][self.nrho + i] > 0:
                                                ion_vpol[ispecies][self.nrho + i] = (
                                                    ion_vpol[ispecies][self.nrho + i]
                                                    + abs(
                                                        self.edge_profiles.profiles_1d[0]
                                                        .ion[jspecies]
                                                        .state[istate]
                                                        .velocity.poloidal[i]
                                                    )
                                                    * self.edge_profiles.profiles_1d[0]
                                                    .ion[jspecies]
                                                    .state[istate]
                                                    .density[i]
                                                    / self.ion_density[ispecies][self.nrho + i]
                                                )
                                        vpol_e_flag = 1
                                except Exception as e:
                                    logger.debug(f"{e}")
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}]."
                                        f"velocity.poloidal could not be read."
                                    )
                    else:
                        if self.edge_profiles.ggd[0].ion[jspecies].multiple_states_flag == 0:
                            try:
                                if (
                                    len(self.edge_profiles.ggd[0].ion[jspecies].velocity[self.gset].poloidal)
                                    == self.erho
                                ):
                                    for i in range(self.erho):
                                        ion_vpol[ispecies][self.nrho + i] = abs(
                                            self.edge_profiles.ggd[0].ion[jspecies].velocity[self.gset].poloidal[i]
                                        )
                                    vpol_e_flag = 1
                            except Exception as e:
                                logger.debug(f"{e}")
                                logger.warning(
                                    "edge_profiles.ggd[:].ion[{jspecies}].velocity.poloidal could not be read."
                                )
                        else:
                            for istate in range(len(self.edge_profiles.ggd[0].ion[jspecies].state)):
                                try:
                                    if (
                                        len(
                                            self.edge_profiles.ggd[0]
                                            .ion[jspecies]
                                            .state[istate]
                                            .velocity[self.gset]
                                            .poloidal
                                        )
                                        == self.erho
                                    ):
                                        for i in range(self.erho):
                                            if self.ion_density[ispecies][self.nrho + i] > 0:
                                                ion_vpol[ispecies][self.nrho + i] = (
                                                    ion_vpol[ispecies][self.nrho + i]
                                                    + abs(
                                                        self.edge_profiles.ggd[0]
                                                        .ion[jspecies]
                                                        .state[istate]
                                                        .velocity[self.gset]
                                                        .poloidal[i]
                                                    )
                                                    * self.edge_profiles.ggd[0]
                                                    .ion[jspecies]
                                                    .state[istate]
                                                    .density[self.gset]
                                                    .values[i]
                                                    / self.ion_density[ispecies][self.nrho + i]
                                                )
                                        vpol_e_flag = 1
                                except Exception as e:
                                    logger.debug(f"{e}")
                                    logger.warning(
                                        f"edge_profiles.ggd[:].ion[{jspecies}].state[{istate}]."
                                        f"velocity.poloidal could not be read."
                                    )

        logger.debug(f"Vpol_flag : {vpol_flag}, Vpol_e_flag : {vpol_e_flag}")
        return {
            "vpol_flag": vpol_flag,
            "vpol_e_flag": vpol_e_flag,
            "ion_vpol": ion_vpol,
        }

    def get_species_list(self):
        import idstools.init_mendeleiev as mend

        # Mendeleiev table
        table_mendeleiev = mend.create_table_mendeleiev()
        if self.nspecies_core > 0:
            # Plasma composition
            species = []
            for ispecies in range(self.nspecies_core):
                if self.n[ispecies] == 1:
                    species.append(table_mendeleiev[self.z[ispecies]][self.a[ispecies]].element)
                else:
                    if self.is_core_profiles_present:
                        species.append(self.core_profiles.profiles_1d[0].ion[ispecies].label)
                    else:
                        if not self.r_out_graph:
                            species.append(self.edge_profiles.profiles_1d[0].ion[ispecies].label)
                        else:
                            species.append(self.edge_profiles.ggd[0].ion[ispecies].label)
            return species
        return None

    def get_n_spec_nver_ne(self):
        if (self.nspecies_core > 0) and self.is_composition_available:
            if self.is_edge_profiles_present and self.is_core_profiles_present:
                logger.debug("Species_mapping :")
                for ispecies in range(self.nspecies_core):
                    if self.species_map[ispecies] != -99:
                        logger.debug(
                            f"Core species {ispecies} is {self.species[ispecies]} and maps to edge species "
                            f"{self.species_map[ispecies]}"
                        )
                    else:
                        logger.debug(
                            f"Core species {ispecies} is {self.species[ispecies]} and does not map to edge species"
                        )

            # Species concentrations
            ntot = 0
            imax = -99
            species_density = [0] * self.nspecies_core
            max_density = -999.0
            nspec_over_ntot = [0] * self.nspecies_core
            nspec_over_ne = [0] * self.nspecies_core
            nspec_over_nmaj = [0] * self.nspecies_core
            if self.is_core_profiles_present:
                for ispecies in range(self.nspecies_core):
                    species_density[ispecies] = sum(
                        self.volume[0 : self.nrho - 1]
                        * self.core_profiles.profiles_1d[0].ion[ispecies].density[0 : self.nrho - 1]
                    )
                    ntot = ntot + species_density[ispecies]
                    if species_density[ispecies] > max_density:
                        max_density = species_density[ispecies]
                        imax = ispecies

                ne = sum(
                    self.volume[0 : self.nrho - 1]
                    * self.core_profiles.profiles_1d[0].electrons.density[0 : self.nrho - 1]
                )

                nspec_over_ntot = species_density / ntot
                nspec_over_ne = species_density / ne
                if imax != -99:
                    nspec_over_nmaj = species_density / species_density[imax]
                else:
                    nspec_over_nmaj = 0

            # When a species appears twice: combine
            for ispecies in range(self.nspecies_core):
                for jspecies in range(self.nspecies_core):
                    if (self.species[jspecies] == self.species[ispecies]) & (jspecies != ispecies):
                        nspec_over_ntot[ispecies] = nspec_over_ntot[ispecies] + nspec_over_ntot[jspecies]
                        nspec_over_ntot[jspecies] = 0
                        nspec_over_ne[ispecies] = nspec_over_ne[ispecies] + nspec_over_ne[jspecies]
                        nspec_over_ne[jspecies] = 0
                        nspec_over_nmaj[ispecies] = nspec_over_nmaj[ispecies] + nspec_over_nmaj[jspecies]
                        nspec_over_nmaj[jspecies] = 0

            # Nice display of plasma composition with species concentrations
            disp_species = "   species:      "
            disp_a = "   a:            "
            disp_z = "   z:            "
            disp_nspec_over_ntot = "   n_over_ntot:  "
            disp_nspec_over_ne = "   n_over_ne:    "
            disp_nspec_over_nmaj = "   n_over_n_maj: "
            for ispecies in range(self.nspecies_core):
                if nspec_over_ne[ispecies] > 0.0:
                    tabsize = 8
                    disp_species = disp_species + self.species[ispecies] + " " * (tabsize - len(self.species[ispecies]))
                    disp_a = (
                        disp_a
                        + format("%.1f" % self.a[ispecies])
                        + " " * (tabsize - len(format("%.1f" % self.a[ispecies])))
                    )
                    disp_z = (
                        disp_z
                        + format("%.1f" % self.z[ispecies])
                        + " " * (tabsize - len(format("%.1f" % self.z[ispecies])))
                    )
                    disp_nspec_over_ntot = (
                        disp_nspec_over_ntot
                        + format("%.3f" % nspec_over_ntot[ispecies])
                        + " " * (tabsize - len(format("%.3f" % nspec_over_ntot[ispecies])))
                    )
                    disp_nspec_over_ne = (
                        disp_nspec_over_ne
                        + format("%.3f" % nspec_over_ne[ispecies])
                        + " " * (tabsize - len(format("%.3f" % nspec_over_ne[ispecies])))
                    )
                    disp_nspec_over_nmaj = (
                        disp_nspec_over_nmaj
                        + format("%.3f" % nspec_over_nmaj[ispecies])
                        + " " * (tabsize - len(format("%.3f" % nspec_over_nmaj[ispecies])))
                    )

            if self.is_core_profiles_present == 1:
                print(
                    "   ------------",
                )
                print(disp_species)
                print(disp_a)
                print(disp_z)
                print(disp_nspec_over_ntot)
                print(disp_nspec_over_ne)
                print(disp_nspec_over_nmaj)
                print("   ------------")

        else:
            nspec_over_ne = [0] * self.nspecies_core
        return nspec_over_ne

    def get_profiles(self):
        # Criteria for significant impurity (in X[imp]/ne concentration)

        profiles = {}
        if self.is_core_profiles_present:
            profiles["rhonorm"] = [0] * self.nrho
            profiles["te"] = [0] * self.nrho
            if self.ti_flag != 0:
                profiles["ti"] = [0] * self.nrho
            profiles["ne"] = [0] * self.nrho
            profiles["zeff"] = [0] * self.nrho
            for i in range(self.nrho):
                profiles["rhonorm"][i] = self.rho_tor_norm[i]
                profiles["te"][i] = self.electron_temperature[i]
                if self.ti_flag != 0:
                    profiles["ti"][i] = self.ion_temperature[i]
                profiles["ne"][i] = self.electron_density[i]
                profiles["zeff"][i] = self.zeff[i]
        if self.is_edge_profiles_present:
            profiles["rhonorm_e"] = [0] * self.erho
            profiles["te_e"] = [0] * self.erho
            if self.ti_e_flag != 0:
                profiles["ti_e"] = [0] * self.erho
            profiles["ne_e"] = [0] * self.erho
            profiles["zeff_e"] = [0] * self.erho
            for i in range(self.erho):
                profiles["rhonorm_e"][i] = self.rho_tor_norm[self.nrho + i]
                profiles["te_e"][i] = self.electron_temperature[self.nrho + i]
                if self.ti_e_flag != 0:
                    profiles["ti_e"][i] = self.ion_temperature[self.nrho + i]
                profiles["ne_e"][i] = self.electron_density[self.nrho + i]
                profiles["zeff_e"][i] = self.zeff[self.nrho + i]

        profiles["n_species"] = {}
        for ispecies in range(self.nspecies_core):
            profiles["n_species"][self.species[ispecies]] = {}
        if self.is_core_profiles_present:
            profiles["ni"] = [0] * self.nrho
            for ispecies in range(self.nspecies_core):
                if self.is_composition_available is True:
                    if self.nspec_over_ne[ispecies] > kinetic_profiles_compute.i_m_p_u_r_i_t_y__l_i_m_i_t:
                        profiles["n_species"][self.species[ispecies]]["density"] = [0] * self.nrho
                        if self.vpol_flag != 0:
                            profiles["n_species"][self.species[ispecies]]["vpol"] = [0] * self.nrho
                        if self.vtor_flag != 0:
                            profiles["n_species"][self.species[ispecies]]["vtor"] = [0] * self.nrho
                        for i in range(self.nrho):
                            profiles["n_species"][self.species[ispecies]]["density"][i] = self.ion_density[ispecies][i]
                            if self.vpol_flag != 0:
                                profiles["n_species"][self.species[ispecies]]["vpol"][i] = self.ion_vpol[ispecies][i]
                            if self.vtor_flag != 0:
                                profiles["n_species"][self.species[ispecies]]["vtor"][i] = self.ion_vtor[ispecies][i]
            for i in range(self.nrho):
                profiles["ni"][i] = profiles["ni"][i] + self.ion_density[ispecies][i]
        if self.is_edge_profiles_present:
            profiles["ni_e"] = [0] * self.erho
            for ispecies in range(self.nspecies_core):
                if self.species_map[ispecies] != -99:
                    profiles["n_species"][self.species[ispecies]]["density_e"] = [0] * self.erho
                    if self.vpol_e_flag != 0:
                        profiles["n_species"][self.species[ispecies]]["vpol_e"] = [0] * self.erho
                    if self.vtor_e_flag != 0:
                        profiles["n_species"][self.species[ispecies]]["vtor_e"] = [0] * self.erho
                    for i in range(self.erho):
                        profiles["n_species"][self.species[ispecies]]["density_e"][i] = self.ion_density[ispecies][
                            self.nrho + i
                        ]
                        if self.vpol_e_flag != 0:
                            profiles["n_species"][self.species[ispecies]]["vpol_e"][i] = self.ion_vpol[ispecies][
                                self.nrho + i
                            ]
                        if self.vtor_e_flag != 0:
                            profiles["n_species"][self.species[ispecies]]["vtor_e"][i] = self.ion_vtor[ispecies][
                                self.nrho + i
                            ]
                if self.species_map[ispecies] != -99:
                    for i in range(self.erho):
                        profiles["ni_e"][i] = profiles["ni_e"][i] + self.ion_density[ispecies][self.nrho + i]
        return profiles

    def get_min_max_velocity_profiles(self):
        # vtor_flag = vtor_profile["vtor_flag"]
        # vtor_e_flag = vtor_profile["vtor_e_flag"]
        # ion_vtor = vtor_profile["ion_vtor"]

        # vpol_flag = vpol_profile["vpol_flag"]
        # vpol_e_flag = vpol_profile["vpol_e_flag"]
        # ion_vpol = vpol_profile["ion_vpol"]
        # Min and max of velocity profiles
        max_vtor = -9e99
        min_vtor = 9e99
        max_vpol = -9e99
        min_vpol = 9e99
        for ispecies in range(self.nspecies_core):
            if self.is_composition_available and (
                self.nspec_over_ne[ispecies] > kinetic_profiles_compute.i_m_p_u_r_i_t_y__l_i_m_i_t
                or not self.is_core_profiles_present
            ):
                if self.vtor_flag != 0:
                    if "vtor" in self.profiles["n_species"][self.species[ispecies]].keys():
                        if max_vtor < max(
                            self.profiles["n_species"][self.species[ispecies]]["vtor"][0 : self.nrho - 1]
                        ):
                            max_vtor = max(
                                self.profiles["n_species"][self.species[ispecies]]["vtor"][0 : self.nrho - 1]
                            )
                        if min_vtor > min(
                            self.profiles["n_species"][self.species[ispecies]]["vtor"][0 : self.nrho - 1]
                        ):
                            min_vtor = min(
                                self.profiles["n_species"][self.species[ispecies]]["vtor"][0 : self.nrho - 1]
                            )
                if self.is_edge_profiles_present and self.species_map[ispecies] != -99 and self.vtor_e_flag != 0:
                    if "vtor_e" in self.profiles["n_species"][self.species[ispecies]].keys():
                        if max_vtor < max(
                            self.profiles["n_species"][self.species[ispecies]]["vtor_e"][0 : self.erho - 1]
                        ):
                            max_vtor = max(
                                self.profiles["n_species"][self.pecies[ispecies]]["vtor_e"][0 : self.erho - 1]
                            )
                        if min_vtor > min(
                            self.profiles["n_species"][self.species[ispecies]]["vtor_e"][0 : self.erho - 1]
                        ):
                            min_vtor = min(
                                self.profiles["n_species"][self.species[ispecies]]["vtor_e"][0 : self.erho - 1]
                            )
                if self.vpol_flag != 0:
                    if "vpol" in self.profiles["n_species"][self.species[ispecies]].keys():
                        if max_vpol < max(
                            self.profiles["n_species"][self.species[ispecies]]["vpol"][0 : self.nrho - 1]
                        ):
                            max_vpol = max(
                                self.profiles["n_species"][self.species[ispecies]]["vpol"][0 : self.nrho - 1]
                            )
                        if min_vpol > min(
                            self.profiles["n_species"][self.species[ispecies]]["vpol"][0 : self.nrho - 1]
                        ):
                            min_vpol = min(
                                self.profiles["n_species"][self.species[ispecies]]["vpol"][0 : self.nrho - 1]
                            )
                if self.is_edge_profiles_present and self.species_map[ispecies] != -99 and self.vpol_e_flag != 0:
                    if "vpol_e" in self.profiles["n_species"][self.species[ispecies]].keys():
                        if max_vpol < max(
                            self.profiles["n_species"][self.species[ispecies]]["vpol_e"][0 : self.erho - 1]
                        ):
                            max_vpol = max(
                                self.profiles["n_species"][self.pecies[ispecies]]["vpol_e"][0 : self.erho - 1]
                            )
                        if min_vpol > min(
                            self.profiles["n_species"][self.species[ispecies]]["vpol_e"][0 : self.erho - 1]
                        ):
                            min_vpol = min(
                                self.profiles["n_species"][self.species[ispecies]]["vpol_e"][0 : self.erho - 1]
                            )

        if self.vtor_flag != 0 or self.vtor_e_flag != 0:
            logger.debug(f"max_vtor : {max_vtor}")
            logger.debug(f"min_vtor : {min_vtor}")
        if self.vpol_flag != 0 or self.vpol_e_flag != 0:
            logger.debug(f"max_vpol : {max_vpol}")
            logger.debug(f"min_vpol : {min_vpol}")

        return {
            "max_vtor": max_vtor,
            "min_vtor": min_vtor,
            "max_vpol": max_vpol,
            "min_vpol": min_vpol,
        }

    def create_wave_form(self, ndim):
        return {"central": [0] * ndim, "edge": [0] * ndim, "rho95": [0] * ndim}

    def get_waveform(self):
        vtor_flag = self.vtor_flag

        vpol_flag = self.vpol_flag
        # Create the dictionary defining the list of waveforms (central values) that can be displayed
        if self.is_core_profiles_present:
            waveform = {}
            waveform["time"] = self.common_time_array
            for ikey in ["te", "ti", "ne", "zeff"]:
                waveform[ikey] = self.create_wave_form(0)

            waveform["te"]["central"] = (
                self.connection.partial_get("core_profiles", "profiles_1d(:)/electrons/temperature(0)") * 1e-3
            )
            if self.ti_flag == 1:
                waveform["ti"]["central"] = (
                    self.connection.partial_get("core_profiles", "profiles_1d(:)/t_i_average(0)") * 1e-3
                )
            else:
                try:
                    waveform["ti"]["central"] = (
                        self.connection.partial_get("core_profiles", "profiles_1d(:)/ion(0)/temperature(0)") * 1e-3
                    )
                except Exception as e:
                    logger.debug(f"{e}")
                    waveform["ti"]["central"] = [np.na_n] * self.common_time_length

            waveform["ne"]["central"] = self.connection.partial_get(
                "core_profiles", "profiles_1d(:)/electrons/density(0)"
            )
            waveform["zeff"]["central"] = self.connection.partial_get("core_profiles", "profiles_1d(:)/zeff(0)")

            waveform["n_species"] = {}
            waveform["ni"] = self.create_wave_form(self.common_time_length)
            for ispecies in range(self.nspecies_core):
                if self.is_composition_available and (
                    self.nspec_over_ne[ispecies] > kinetic_profiles_compute.i_m_p_u_r_i_t_y__l_i_m_i_t
                ):
                    waveform["n_species"][self.species[ispecies]] = {
                        "density": self.create_wave_form(0),
                        "vpol": self.create_wave_form(0),
                        "vtor": self.create_wave_form(0),
                    }

                    try:
                        waveform["n_species"][self.species[ispecies]]["density"]["central"] = (
                            self.connection.partial_get(
                                "core_profiles",
                                f"profiles_1d(:)/ion({ispecies})/density(0)",
                            )
                        )
                        if vpol_flag == 1:
                            waveform["n_species"][self.species[ispecies]]["vpol"]["central"] = (
                                self.connection.partial_get(
                                    "core_profiles",
                                    f"profiles_1d(:)/ion({ispecies})/velocity/poloidal(0)",
                                )
                            )
                        elif vpol_flag == 2:
                            waveform["n_species"][self.species[ispecies]]["vpol"]["central"] = (
                                self.connection.partial_get(
                                    "core_profiles",
                                    f"profiles_1d(:)/ion({ispecies})/velocity_pol(0)",
                                )
                            )
                        if vtor_flag == 1:
                            waveform["n_species"][self.species[ispecies]]["vtor"]["central"] = (
                                self.connection.partial_get(
                                    "core_profiles",
                                    f"profiles_1d(:)/ion({ispecies})/velocity/toroidal(0)",
                                )
                            )
                        elif vtor_flag == 2:
                            waveform["n_species"][self.species[ispecies]]["vtor"]["central"] = (
                                self.connection.partial_get(
                                    "core_profiles",
                                    f"profiles_1d(:)/ion({ispecies})/velocity_tor(0)",
                                )
                            )
                    except Exception as e:
                        logger.debug(f"{e}")
                        waveform["n_species"][self.species[ispecies]]["density"]["central"] = [
                            np.na_n
                        ] * self.common_time_length
                        waveform["n_species"][self.species[ispecies]]["vpol"]["central"] = [
                            np.na_n
                        ] * self.common_time_length
                        waveform["n_species"][self.species[ispecies]]["vtor"]["central"] = [
                            np.na_n
                        ] * self.common_time_length

                    for itime in range(self.common_time_length):
                        waveform["ni"]["central"][itime] = (
                            waveform["ni"]["central"][itime]
                            + waveform["n_species"][self.species[ispecies]]["density"]["central"][itime]
                        )
            return waveform
        return None
