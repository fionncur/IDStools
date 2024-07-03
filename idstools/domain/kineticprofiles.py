import logging

import imas
import numpy as np

from idstools.compute.common import getNearestTime
from idstools.compute.core_profiles import CoreProfilesCompute
from idstools.compute.edge_profiles import EdgeProfilesCompute
from idstools.compute.equilibrium import EquilibriumCompute

logger = logging.getLogger("module")


class KineticProfilesCompute:
    IMPURITY_LIMIT = 0.001

    def __init__(self):
        self.connection = None
        self.edgeRequired = None

        self.core_profiles = None
        self.edge_profiles = None
        self.equilibrium = None

        self.isCoreProfilesPresent = True
        self.isEdgeProfilesPresent = False
        self.isEquilibriumPresent = False

        self.r_out_graph = False
        self.commonTimeLength = None
        self.commonTimeArray = None

        self.initialised = None

        self.isCompositionAvailable = True
        self.gset = None
        self.nrho = None
        self.mrho = None
        self.erho = None
        self.nspeciesCore = None
        self.nspeciesEdge = None
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

    def analyze(self, connection, edgeRequired=False, timeSlice=-99.0):
        self.connection = connection
        self.edgeRequired = edgeRequired
        self.initialised = self.checkIDSes()
        self.fillIDSes(timeSlice)

        self.edgeProfilesCompute = EdgeProfilesCompute(self.edge_profiles)
        self.coreProfilesCompute = CoreProfilesCompute(self.core_profiles)
        self.equlibriumCompute = EquilibriumCompute(self.equilibrium)

        self.gset = self.getgset()
        (
            self.nrho,
            self.mrho,
            self.erho,
        ) = self.getRhoTorNorm()
        self.nspeciesCore, self.nspeciesEdge = self.getSpecies()

        rhoOrROutboardProfile = self.getRhoOrROutboardProfile()
        self.xbeg = rhoOrROutboardProfile["xbeg"]
        self.xend = rhoOrROutboardProfile["xend"]
        self.rho_tor_norm = rhoOrROutboardProfile["rho_tor_norm"]

        self.nspeciesCore, self.nspeciesCoreEdge = self.getSpecies()
        self.a = self.getSpeciesANumber()  # Species A number (not mandatory)
        self.z = self.getSpeciesZNumber()  # Species Z number (not mandatory)
        self.n = self.getSpeciesAtoms_n()  # Number of atoms per species (not mandatory)
        self.species_map = self.getSpeciesMap()
        self.volume = self.getVolumeProfile()  # Volume profile (not mandatory)
        self.zeff = self.getZeffProfile()  # Zeff profile (not mandatory)
        self.electron_density = self.getneProfile()  # Ne profile (not mandatory)
        self.electron_temperature = self.getteProfile()  # Te profile (not mandatory)
        self.ti_flag, self.ti_e_flag = self.gettiFlag()  # Ti profile (not mandatory)
        self.ion_temperature = self.getIonTemperature()  # ion temerature
        self.ion_density = self.getIonDensity()  # Ni profile (not mandatory)
        vtor_profile = self.getVTorProfile()  # Vtor profile (not mandatory)
        self.vtor_flag = vtor_profile["vtor_flag"]
        self.vtor_e_flag = vtor_profile["vtor_e_flag"]
        self.ion_vtor = vtor_profile["ion_vtor"]
        vpol_profile = self.getVpolProfile()  # Vpol profile (not mandatory)
        self.vpol_flag = vpol_profile["vpol_flag"]
        self.vpol_e_flag = vpol_profile["vpol_e_flag"]
        self.ion_vpol = vpol_profile["ion_vpol"]
        self.species = self.getSpeciesList()
        self.nspec_over_ne = self.getNSpecNverNe()

        self.profiles = self.getProfiles()  # Create the dictionary defining the list of profiles

        velocityProfiles = self.getMinMaxVelocityProfiles()  # Min and max of velocity profiles
        self.max_vtor = velocityProfiles["max_vtor"]
        self.min_vtor = velocityProfiles["min_vtor"]
        self.max_vpol = velocityProfiles["max_vpol"]
        self.min_vpol = velocityProfiles["min_vpol"]

        self.waveform = self.getWaveform()  # Create the dictionary defining the list of waveforms (central values)

    def getIDS(self, idsName=""):
        idsPresent = False
        idsObject = None
        if idsName:
            try:
                idsObject = eval(f"imas.{idsName}()")  # To initialise the empty IDS structure
                idsObject.time = self.connection.partial_get(idsName, "time")
                if idsObject.time is not None:
                    if len(idsObject.time) > 0:
                        idsPresent = True
                else:
                    logger.critical(f"No {idsName} IDS in the data-entry.")
                    idsPresent = False
            except Exception as e:
                logger.critical(f"The {idsName} IDS is absent from the input data-entry.")
                idsPresent = False
        return idsObject, idsPresent

    def checkIDSes(self):
        self.core_profiles, self.isCoreProfilesPresent = self.getIDS("core_profiles")
        if self.edgeRequired:
            self.edge_profiles, self.isEdgeProfilesPresent = self.getIDS("edge_profiles")
            if self.isCoreProfilesPresent:
                logger.info("Found adjoining edge_profiles. Will attempt to add to plots.")
            else:
                logger.info("Found edge_profiles IDS in data-entry. Will only plot edge data.")
        self.equilibrium, self.isEquilibriumPresent = self.getIDS("equilibrium")

        if not self.isCoreProfilesPresent and not self.isEdgeProfilesPresent:
            logger.critical("No data found to plot. --> Abort.")
            logger.critical("----> Aborted.")
            return None
        return True

    def fillIDSes(self, timeSlice=-99.0):
        # Search for adequate time slice for display
        if self.isCoreProfilesPresent:
            self.commonTimeLength = len(self.core_profiles.time)
            self.commonTimeArray = self.core_profiles.time
        else:
            self.commonTimeLength = len(self.edge_profiles.time)
            self.commonTimeArray = self.edge_profiles.time
        self.commonTime = timeSlice
        commonTimeIndex, commonTimeValue = getNearestTime(self.commonTimeArray, timeSlice)

        self.commonTime = commonTimeValue

        # Read 1D-profiles for this time slice
        if self.isCoreProfilesPresent:
            self.core_profiles.profiles_1d.resize(1)
            self.core_profiles.profiles_1d[0] = self.connection.partial_get(
                "core_profiles", f"profiles_1d({commonTimeIndex})"
            )

        # Read equilibrium data for this time slice if present
        if self.isEquilibriumPresent:
            # ntimeEquilibrium = len(self.equilibrium.time)
            timeArrayEquilibrium = self.equilibrium.time
            timeIndexEquilibrium, timeValueEquilibrium = getNearestTime(timeArrayEquilibrium, self.commonTime)

        # Add 1D-profiles edge data if present

        if self.isEdgeProfilesPresent:
            # ntimeEdgeProfiles = len(self.edge_profiles.time)
            timeArrayEdgeProfiles = self.edge_profiles.time
            timeIndexEdgeProfiles, timeValueEdgeProfiles = getNearestTime(timeArrayEdgeProfiles, self.commonTime)

            # Read edge_profile data for this time slice
            try:
                self.edge_profiles.profiles_1d.resize(1)
                self.edge_profiles.profiles_1d[0] = self.connection.partial_get(
                    "edge_profiles", f"profiles_1d({timeIndexEdgeProfiles})"
                )
                teme = timeValueEdgeProfiles
            except Exception as e:
                logger.warning("No profiles_1d information found in edge_profiles IDS.")
                if self.isEquilibriumPresent and len(self.equilibrium.time) > 0:
                    self.equilibrium.time_slice.resize(1)
                    self.equilibrium.time_slice[0] = self.connection.partial_get(
                        "equilibrium", f"time_slice({timeIndexEquilibrium})"
                    )
                    # tqme = timeValueEquilibrium
                    if len(self.equilibrium.time_slice[0].profiles_1d.r_outboard) > 0 or not self.isCoreProfilesPresent:
                        self.edge_profiles.grid_ggd.resize(1)
                        try:
                            self.edge_profiles.grid_ggd[0] = self.connection.partial_get(
                                "edge_profiles",
                                f"grid_ggd({timeIndexEdgeProfiles})",
                            )
                        except Exception as e:
                            self.isEdgeProfilesPresent = False
                            logger.warning("No grid_ggd information found in edge_profiles IDS.")
                        self.edge_profiles.ggd.resize(1)
                        try:
                            self.edge_profiles.ggd[0] = self.connection.partial_get(
                                "edge_profiles", f"ggd({timeIndexEdgeProfiles})"
                            )
                        except Exception as e:
                            self.isEdgeProfilesPresent = False
                            logger.warning("No ggd information found in edge_profiles IDS.")
                        if self.isEdgeProfilesPresent:
                            self.r_out_graph = True
                            logger.info("Attempting to use R_outboard coordinate instead.")
                    else:
                        if self.isCoreProfilesPresent:
                            self.isEdgeProfilesPresent = False
                else:
                    if self.isCoreProfilesPresent:
                        self.isEdgeProfilesPresent = False
                    else:
                        self.edge_profiles.grid_ggd.resize(1)
                        try:
                            self.edge_profiles.grid_ggd[0] = self.connection.partial_get(
                                "edge_profiles",
                                f"grid_ggd({timeIndexEdgeProfiles})",
                            )
                        except Exception as e:
                            self.isEdgeProfilesPresent = False
                            logger.warning("No grid_ggd information found in edge_profiles IDS.")
                        self.edge_profiles.ggd.resize(1)
                        try:
                            self.edge_profiles.ggd[0] = self.connection.partial_get(
                                "edge_profiles", f"ggd({timeIndexEdgeProfiles})"
                            )
                        except Exception as e:
                            self.isEdgeProfilesPresent = False
                            logger.warning("No ggd information found in edge_profiles IDS.")
                        if self.isEdgeProfilesPresent:
                            self.r_out_graph = True
                            logger.info("Attempting to use R coordinate instead.")

    def getgset(self):
        if self.r_out_graph:
            gset = self.edgeProfilesCompute.getOuterMidplaneArrayIndex()
            if gset is None:
                logger.warning("Abandoning edge plots !")
                self.isEdgeProfilesPresent = False
                self.r_out_graph = False
            try:
                if self.edge_profiles.midplane.index != 1 and self.r_out_graph and self.isCoreProfilesPresent:
                    logger.warning("Edge and core profile midplane coordinates are not aligned!")
            except Exception as e:
                logger.warning("Edge_profiles midplane location not specified! Coordinates may be misaligned.")
            return gset
        return None

    def getRhoOrROutboardProfile(self):
        xbeg = 99.0
        xend = 0
        rho_tor_norm = [0] * (self.nrho + self.erho)
        if not self.r_out_graph and self.isCoreProfilesPresent:
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
        elif self.isCoreProfilesPresent:
            for i in range(self.nrho):
                rho_tor_norm[i] = self.equilibrium.time_slice[0].profiles_1d.r_outboard[self.mrho + i]
            xbeg = min(xbeg, rho_tor_norm[self.nrho - 1], rho_tor_norm[0])
            xend = max(xend, rho_tor_norm[self.nrho - 1], rho_tor_norm[0])

        if self.isEdgeProfilesPresent:
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
                ) and self.isEdgeProfilesPresent:
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
                        f"Unexpected dimensionality of Outer Midplane GGD subset : {self.edge_profiles.grid_ggd[0].grid_subset[self.gset].dimension}"
                    )
                    logger.warning("Abandoning edge plots !")
                    self.isEdgeProfilesPresent = False
        return {"xbeg": xbeg, "xend": xend, "rho_tor_norm": rho_tor_norm}

    def getSpecies(self):
        nspeciesCore = 0
        if self.isCoreProfilesPresent:
            try:
                nspeciesCore = len(self.core_profiles.profiles_1d[0].ion)
            except Exception as e:
                logger.critical("core_profiles.profiles_1d[0].ion could not be read.")
                return None

        nspeciesEdge = nspeciesCore
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                nspeciesEdge = len(self.edge_profiles.profiles_1d[0].ion)
            else:
                nspeciesEdge = len(self.edge_profiles.ggd[0].ion)
        if nspeciesCore != nspeciesEdge and self.isCoreProfilesPresent and self.isEdgeProfilesPresent:
            logger.warning("Warning: list of species in core and edge profiles data do not match!")
        if not self.isCoreProfilesPresent:
            nspeciesCore = nspeciesEdge

        return nspeciesCore, nspeciesEdge

    def getSpeciesANumber(self):
        a = [0] * self.nspeciesCore
        if self.isCoreProfilesPresent:
            try:
                for ispecies in range(self.nspeciesCore):
                    a[ispecies] = int(self.core_profiles.profiles_1d[0].ion[ispecies].element[0].a)
            except Exception as e:
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].a could not be read.")
                self.isCompositionAvailable = False  # plot_compo
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspeciesCoreEdge):
                        a[ispecies] = int(self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].a)
                except Exception as e:
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].a could not be read.")
                    self.isCompositionAvailable = False
            else:
                try:
                    for ispecies in range(self.nspeciesCoreEdge):
                        a[ispecies] = int(self.edge_profiles.ggd[0].ion[ispecies].element[0].a)
                except Exception as e:
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].a could not be read.")
                    self.isCompositionAvailable = False
        return a

    def getSpeciesZNumber(self):
        z = [0] * self.nspeciesCore
        if self.isCoreProfilesPresent:
            try:
                for ispecies in range(self.nspeciesCore):
                    z[ispecies] = int(self.core_profiles.profiles_1d[0].ion[ispecies].element[0].z_n)
            except Exception as e:
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].z_n could not be read.")
                self.isCompositionAvailable = False
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspeciesEdge):
                        z[ispecies] = int(self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].z_n)
                except Exception as e:
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].z_n could not be read.")
                    self.isCompositionAvailable = False
            else:
                try:
                    for ispecies in range(self.nspeciesEdge):
                        z[ispecies] = int(self.edge_profiles.ggd[0].ion[ispecies].element[0].z_n)
                except Exception as e:
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].z_n could not be read.")
                    self.isCompositionAvailable = False
        return z

    def getSpeciesAtoms_n(self):
        n = [1] * self.nspeciesCore
        if self.isCoreProfilesPresent:
            try:
                for ispecies in range(self.nspeciesCore):
                    n[ispecies] = self.core_profiles.profiles_1d[0].ion[ispecies].element[0].atoms_n
            except Exception as e:
                logger.warning("core_profiles.profiles_1d[:].ion[0].element[0].atoms_n could not be read.")
                logger.warning("Value of 1 assumed.")
        else:
            if not self.r_out_graph:
                try:
                    for ispecies in range(self.nspeciesEdge):
                        n[ispecies] = self.edge_profiles.profiles_1d[0].ion[ispecies].element[0].atoms_n
                except Exception as e:
                    logger.warning("edge_profiles.profiles_1d[:].ion[0].element[0].atoms_n could not be read.")
                    logger.warning("Value of 1 assumed.")
            else:
                try:
                    for ispecies in range(self.nspeciesEdge):
                        n[ispecies] = self.edge_profiles.ggd[0].ion[ispecies].element[0].atoms_n
                except Exception as e:
                    logger.warning("edge_profiles.ggd[:].ion[0].element[0].atoms_n could not be read.")
                    logger.warning("Value of 1 assumed.")
        return n

    def getSpeciesMap(self):
        if self.isEdgeProfilesPresent:
            species_map = [-99] * self.nspeciesCore
            for ispecies in range(self.nspeciesCore):
                for jspecies in range(self.nspeciesEdge):
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
                if species_map[ispecies] == -99 and self.isCoreProfilesPresent == 1:
                    logger.warning(
                        "Core_profiles species "
                        + self.core_profiles.profiles_1d[0].ion[ispecies].label
                        + " has no partner in edge_profiles!"
                    )
            self.species_map = species_map
            return species_map
        return None

    def getRhoTorNorm(self):
        nrho = 0
        mrho = 0
        if not self.r_out_graph and self.isCoreProfilesPresent:
            nrho = self.coreProfilesCompute.getnrho()
            if nrho is None or nrho == 0:
                logger.error("core_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty.")
                logger.error("----> Aborted.")
                exit()
        else:
            if self.isCoreProfilesPresent:
                if len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm) == len(
                    self.core_profiles.profiles_1d[0].grid.rho_tor_norm
                ):
                    nrho = len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm)
                else:
                    mrho = self.equlibriumCompute.getmrho()
                    nrho = len(self.equilibrium.time_slice[0].profiles_1d.rho_tor_norm) - mrho

        erho = 0
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                erho = self.coreProfilesCompute.getnrho()
                if nrho is None or nrho == 0:
                    logger.warning("edge_profiles.profiles_1d[:].grid.rho_tor_norm and rho_tor are empty.")
            else:
                erho = len(self.edge_profiles.grid_ggd[0].grid_subset[self.gset].element)
        return nrho, mrho, erho

    def getVolumeProfile(self):
        volume = [0] * (self.nrho + self.erho)
        if self.isCoreProfilesPresent:
            if len(self.core_profiles.profiles_1d[0].grid.volume) == self.nrho:
                for i in range(self.nrho):
                    volume[i] = self.core_profiles.profiles_1d[0].grid.volume[i]
            else:
                try:
                    equilibrium = self.connection.equilibrium
                    equilibrium.time_slice[0].profiles_1d.volume = self.connection.partial_get(
                        "equilibrium",
                        f"time_slice({self.commonTimeIndex})/profiles_1d/volume",
                    )
                    for i in range(self.nrho):
                        volume[i] = equilibrium.time_slice[0].profiles_1d.volume[i]
                    if len(volume) == len(self.core_profiles.profiles_1d[0].electrons.density):
                        logger.warning("   core_profiles.profiles_1d[:].grid.volume could not be read.")
                        logger.warning("   ----> equilibrium.time_slice[:].profiles_1d.volume used instead.")
                        logger.warning("   (possible because the resolution is the same, but maybe not correct)")
                except Exception as e:
                    logger.warning("core_profiles.profiles_1d[:].grid.volume could not be read.")
                    self.isCompositionAvailable = False
        if self.isEdgeProfilesPresent and not self.r_out_graph:
            for i in range(self.erho):
                volume[self.nrho + i] = self.edge_profiles.profiles_1d[0].grid.volume[i]
        return volume

    def getZeffProfile(self):
        zeff = [0] * (self.nrho + self.erho)
        if self.isCoreProfilesPresent:
            if len(self.core_profiles.profiles_1d[0].zeff) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].zeff could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, zeff = {len(self.core_profiles.profiles_1d[0].zeff)}"
                )
                self.core_profiles.profiles_1d[0].zeff = np.asarray([np.NaN] * self.nrho)
            for i in range(self.nrho):
                zeff[i] = self.core_profiles.profiles_1d[0].zeff[i]
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].zeff) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].zeff could not be read.")
                    self.edge_profiles.profiles_1d[0].zeff = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    zeff[self.nrho + i] = self.edge_profiles.profiles_1d[0].zeff[i]
            else:
                if len(self.edge_profiles.ggd[0].zeff[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].zeff could not be read.")
                    self.edge_profiles.ggd[0].zeff[self.gset].values = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    zeff[self.nrho + i] = self.edge_profiles.ggd[0].zeff[self.gset].values[i]
        return zeff

    def getneProfile(self):
        electron_density = [0] * (self.nrho + self.erho)
        if self.isCoreProfilesPresent:
            if len(self.core_profiles.profiles_1d[0].electrons.density) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].electrons.density could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, electrons.density = {len(self.core_profiles.profiles_1d[0].electrons.density)}"
                )
                self.core_profiles.profiles_1d[0].electrons.density = np.asarray([np.NaN] * self.nrho)
            for i in range(self.nrho):
                electron_density[i] = self.core_profiles.profiles_1d[0].electrons.density[i]
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].electrons.density) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].electrons.density could not be read.")
                    self.edge_profiles.profiles_1d[0].electrons.density = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    electron_density[self.nrho + i] = self.edge_profiles.profiles_1d[0].electrons.density[i]
            else:
                if len(self.edge_profiles.ggd[0].electrons.density[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].electrons.density could not be read.")
                    self.edge_profiles.ggd[0].electrons.density[self.gset].values = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    electron_density[self.nrho + i] = self.edge_profiles.ggd[0].electrons.density[self.gset].values[i]
        return electron_density

    def getteProfile(self):
        electron_temperature = [0] * (self.nrho + self.erho)
        if self.isCoreProfilesPresent:
            if len(self.core_profiles.profiles_1d[0].electrons.temperature) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].electrons.temperature could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, electrons.temperature = {len(self.core_profiles.profiles_1d[0].electrons.temperature)}"
                )
                self.core_profiles.profiles_1d[0].electrons.temperature = np.asarray([np.NaN] * self.nrho)
            for i in range(self.nrho):
                electron_temperature[i] = self.core_profiles.profiles_1d[0].electrons.temperature[i] * 1.0e-3
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].electrons.temperature) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].electrons.temperature could not be read.")
                    self.edge_profiles.profiles_1d[0].electrons.temperature = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    electron_temperature[self.nrho + i] = (
                        self.edge_profiles.profiles_1d[0].electrons.temperature[i] * 1.0e-3
                    )
            else:
                if len(self.edge_profiles.ggd[0].electrons.temperature[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].electrons.temperature could not be read.")
                    self.edge_profiles.ggd[0].electrons.temperature[self.gset].values = np.asarray([np.NaN] * self.erho)
                for i in range(self.erho):
                    electron_temperature[self.nrho + i] = (
                        self.edge_profiles.ggd[0].electrons.temperature[self.gset].values[i] * 1.0e-3
                    )
        return electron_temperature

    def gettiFlag(self):
        ti_flag = 0
        if self.isCoreProfilesPresent:
            if len(self.core_profiles.profiles_1d[0].t_i_average) != self.nrho:
                logger.warning("core_profiles.profiles_1d[:].t_i_average could not be read.")
                logger.warning(
                    f"Size mismatch: rho_tor_norm = {self.nrho}, t_i_average = {len(self.core_profiles.profiles_1d[0].t_i_average)}"
                )
                self.core_profiles.profiles_1d[0].t_i_average = np.asarray([np.NaN] * self.nrho)
            else:
                ti_flag = 1
        ti_e_flag = 0
        if self.isEdgeProfilesPresent:
            if not self.r_out_graph:
                if len(self.edge_profiles.profiles_1d[0].t_i_average) < 1:
                    logger.warning("edge_profiles.profiles_1d[:].t_i_average could not be read.")
                    self.edge_profiles.profiles_1d[0].t_i_average = np.asarray([np.NaN] * self.erho)
                else:
                    ti_e_flag = 1
            else:
                if len(self.edge_profiles.ggd[0].t_i_average[self.gset].values) < 1:
                    logger.warning("edge_profiles.ggd[:].t_i_average could not be read.")
                    self.edge_profiles.ggd[0].t_i_average[self.gset].values = np.asarray([np.NaN] * self.erho)
                else:
                    ti_e_flag = 1

        if ti_flag == 0:
            for ispecies in range(self.nspeciesCore):
                if self.isCoreProfilesPresent:
                    if len(self.core_profiles.profiles_1d[0].ion[ispecies].temperature) != self.nrho:
                        logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].temperature could not be read.")
                        logger.warning(
                            f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].temperature = {len(self.core_profiles.profiles_1d[0].ion[ispecies].temperature)}"
                        )
                        self.core_profiles.profiles_1d[0].ion[ispecies].temperature = np.asarray([np.NaN] * self.nrho)
                    else:
                        ti_flag = 2
                if self.isEdgeProfilesPresent and ti_e_flag == 0:
                    jspecies = self.species_map[ispecies]
                    if jspecies != -99:
                        if not self.r_out_graph:
                            if len(self.edge_profiles.profiles_1d[0].ion[jspecies].temperature) < 1:
                                if ti_e_flag != 1:
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].temperature could not be read."
                                    )
                                    self.edge_profiles.profiles_1d[0].ion[jspecies].temperature = np.asarray(
                                        [np.NaN] * self.erho
                                    )
                            else:
                                ti_e_flag = 2
                        else:
                            if len(self.edge_profiles.ggd[0].ion[jspecies].temperature) < 1:
                                if ti_e_flag != 1:
                                    logger.warning("edge_profiles.ggd[:].ion[:].temperature could not be read.")
                                    self.edge_profiles.ggd[0].ion[jspecies].temperature[self.gset].values = np.asarray(
                                        [np.NaN] * self.erho
                                    )
                            else:
                                ti_e_flag = 2

        logger.info(f"Ti_flag : {ti_flag}, Ti_e_flag : {ti_e_flag}")
        self.ti_flag = ti_flag
        self.ti_e_flag = ti_e_flag
        return ti_flag, ti_e_flag

    def getIonTemperature(self):
        ion_temperature = [0] * (self.nrho + self.erho)
        if self.ti_flag == 1:
            for i in range(self.nrho):
                ion_temperature[i] = self.core_profiles.profiles_1d[0].t_i_average[i] * 1.0e-3
        elif self.ti_flag == 2:
            for i in range(self.nrho):
                ion_temperature[i] = self.core_profiles.profiles_1d[0].ion[0].temperature[i] * 1.0e-3
        if self.isEdgeProfilesPresent:
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

    def getIonDensity(self):
        ion_density = {}
        for ispecies in range(self.nspeciesCore):
            ion_density[ispecies] = [0] * (self.nrho + self.erho)
            if self.isCoreProfilesPresent:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].density) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].density could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].density = {len(self.core_profiles.profiles_1d[0].ion[ispecies].density)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].density = np.asarray([np.NaN] * self.nrho)
                for i in range(self.nrho):
                    ion_density[ispecies][i] = self.core_profiles.profiles_1d[0].ion[ispecies].density[i]
            if self.isEdgeProfilesPresent:
                jspecies = self.species_map[ispecies]
                if jspecies != -99:
                    if not self.r_out_graph:
                        if self.edge_profiles.profiles_1d[0].ion[jspecies].multiple_states_flag == 0:
                            if len(self.edge_profiles.profiles_1d[0].ion[jspecies].density) < 1:
                                logger.warning(
                                    f"edge_profiles.profiles_1d[:].ion[{jspecies}].density could not be read."
                                )
                                self.edge_profiles.profiles_1d[0].ion[jspecies].density = np.asarray(
                                    [np.NaN] * self.erho
                                )
                            for i in range(self.erho):
                                ion_density[ispecies][self.nrho + i] = (
                                    self.edge_profiles.profiles_1d[0].ion[jspecies].density[i]
                                )
                        else:
                            for istate in range(len(self.edge_profiles.profiles_1d[0].ion[jspecies].state)):
                                if len(self.edge_profiles.profiles_1d[0].ion[jspecies].state[istate].density) < 1:
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}].density could not be read."
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
                                    [np.NaN] * self.erho
                                )
                            for i in range(self.erho):
                                ion_density[ispecies][self.nrho + i] = (
                                    self.edge_profiles.ggd[0].ion[jspecies].density[self.gset].values[i]
                                )
                        else:
                            for istate in range(len(self.edge_profiles.ggd[0].ion[jspecies].state)):
                                if len(self.edge_profiles.ggd[0].ion[jspecies].state[istate].density) < 1:
                                    logger.warning(
                                        f"edge_profiles.ggd[:].ion[{jspecies}].state[{istate}].density could not be read."
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

    def getVTorProfile(self):
        vtor_flag = 0
        vtor_e_flag = 0
        ion_vtor = {}
        for ispecies in range(self.nspeciesCore):
            ion_vtor[ispecies] = [0] * (self.nrho + self.erho)
            if self.isCoreProfilesPresent:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity.toroidal could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity.toroidal = {len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal = np.asarray([np.NaN] * self.nrho)
                else:
                    vtor_flag = 1
                    for i in range(self.nrho):
                        ion_vtor[ispecies][i] = abs(
                            self.core_profiles.profiles_1d[0].ion[ispecies].velocity.toroidal[i]
                        )
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity_tor could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity_tor = {len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor = np.asarray([np.NaN] * self.nrho)
                else:
                    if vtor_flag == 0:
                        vtor_flag = 2
                        for i in range(self.nrho):
                            ion_vtor[ispecies][i] = abs(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_tor[i])
            if self.isEdgeProfilesPresent:
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
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}].velocity.toroidal could not be read."
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
                                        logger.warning(
                                            f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}].velocity_tor could not be read."
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
                                    logger.warning(
                                        f"edge_profiles.ggd[:].ion[{jspecies}].state[{istate}].velocity.toroidal could not be read."
                                    )

        logger.debug(f"Vtor_flag : {vtor_flag}, Vtor_e_flag : {vtor_e_flag}")
        return {
            "vtor_flag": vtor_flag,
            "vtor_e_flag": vtor_e_flag,
            "ion_vtor": ion_vtor,
        }

    def getVpolProfile(self):
        vpol_flag = 0
        vpol_e_flag = 0
        ion_vpol = {}
        for ispecies in range(self.nspeciesCore):
            ion_vpol[ispecies] = [0] * (self.nrho + self.erho)
            if self.isCoreProfilesPresent:
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity.poloidal could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity.poloidal = {len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal = np.asarray([np.NaN] * self.nrho)
                else:
                    vpol_flag = 1
                    for i in range(self.nrho):
                        ion_vpol[ispecies][i] = abs(
                            self.core_profiles.profiles_1d[0].ion[ispecies].velocity.poloidal[i]
                        )
                if len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol) != self.nrho:
                    logger.warning(f"core_profiles.profiles_1d[:].ion[{ispecies}].velocity_pol could not be read.")
                    logger.warning(
                        f"Size mismatch: rho_tor_norm = {self.nrho}, ion[{ispecies}].velocity_pol = {len(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol)}"
                    )
                    self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol = np.asarray([np.NaN] * self.nrho)
                else:
                    if vpol_flag == 0:
                        vpol_flag = 2
                        for i in range(self.nrho):
                            ion_vpol[ispecies][i] = abs(self.core_profiles.profiles_1d[0].ion[ispecies].velocity_pol[i])
            if self.isEdgeProfilesPresent:
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
                                    logger.warning(
                                        f"edge_profiles.profiles_1d[:].ion[{jspecies}].state[{istate}].velocity.poloidal could not be read."
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
                                    logger.warning(
                                        "edge_profiles.ggd[:].ion[{jspecies}].state[{istate}].velocity.poloidal could not be read."
                                    )

        logger.debug(f"Vpol_flag : {vpol_flag}, Vpol_e_flag : {vpol_e_flag}")
        return {
            "vpol_flag": vpol_flag,
            "vpol_e_flag": vpol_e_flag,
            "ion_vpol": ion_vpol,
        }

    def getSpeciesList(self):
        import idstools.init_mendeleiev as mend

        # Mendeleiev table
        table_mendeleiev = mend.create_table_mendeleiev()
        if self.nspeciesCore > 0:
            # Plasma composition
            species = []
            for ispecies in range(self.nspeciesCore):
                if self.n[ispecies] == 1:
                    species.append(table_mendeleiev[self.z[ispecies]][self.a[ispecies]].element)
                else:
                    if self.isCoreProfilesPresent:
                        species.append(self.core_profiles.profiles_1d[0].ion[ispecies].label)
                    else:
                        if not self.r_out_graph:
                            species.append(self.edge_profiles.profiles_1d[0].ion[ispecies].label)
                        else:
                            species.append(self.edge_profiles.ggd[0].ion[ispecies].label)
            return species
        return None

    def getNSpecNverNe(self):
        if (self.nspeciesCore > 0) and self.isCompositionAvailable:
            if self.isEdgeProfilesPresent and self.isCoreProfilesPresent:
                logger.debug("Species_mapping :")
                for ispecies in range(self.nspeciesCore):
                    if self.species_map[ispecies] != -99:
                        logger.debug(
                            f"Core species {ispecies} is {self.species[ispecies]} and maps to edge species {self.species_map[ispecies]}"
                        )
                    else:
                        logger.debug(
                            f"Core species {ispecies} is {self.species[ispecies]} and does not map to edge species"
                        )

            # Species concentrations
            ntot = 0
            imax = -99
            species_density = [0] * self.nspeciesCore
            max_density = -999.0
            nspec_over_ntot = [0] * self.nspeciesCore
            nspec_over_ne = [0] * self.nspeciesCore
            nspec_over_nmaj = [0] * self.nspeciesCore
            if self.isCoreProfilesPresent:
                for ispecies in range(self.nspeciesCore):
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
            for ispecies in range(self.nspeciesCore):
                for jspecies in range(self.nspeciesCore):
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
            for ispecies in range(self.nspeciesCore):
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

            if self.isCoreProfilesPresent == 1:
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
            nspec_over_ne = [0] * self.nspeciesCore
        return nspec_over_ne

    def getProfiles(self):
        # Criteria for significant impurity (in X[imp]/ne concentration)

        profiles = {}
        if self.isCoreProfilesPresent:
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
        if self.isEdgeProfilesPresent:
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
        for ispecies in range(self.nspeciesCore):
            profiles["n_species"][self.species[ispecies]] = {}
        if self.isCoreProfilesPresent:
            profiles["ni"] = [0] * self.nrho
            for ispecies in range(self.nspeciesCore):
                if self.isCompositionAvailable is True:
                    if self.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT:
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
        if self.isEdgeProfilesPresent:
            profiles["ni_e"] = [0] * self.erho
            for ispecies in range(self.nspeciesCore):
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

    def getMinMaxVelocityProfiles(self):
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
        for ispecies in range(self.nspeciesCore):
            if self.isCompositionAvailable and (
                self.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT or not self.isCoreProfilesPresent
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
                if self.isEdgeProfilesPresent and self.species_map[ispecies] != -99 and self.vtor_e_flag != 0:
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
                if self.isEdgeProfilesPresent and self.species_map[ispecies] != -99 and self.vpol_e_flag != 0:
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

    def createWaveForm(self, ndim):
        return {"central": [0] * ndim, "edge": [0] * ndim, "rho95": [0] * ndim}

    def getWaveform(self):
        vtor_flag = self.vtor_flag

        vpol_flag = self.vpol_flag
        # Create the dictionary defining the list of waveforms (central values) that can be displayed
        if self.isCoreProfilesPresent:
            waveform = {}
            waveform["time"] = self.commonTimeArray
            for ikey in ["te", "ti", "ne", "zeff"]:
                waveform[ikey] = self.createWaveForm(0)

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
                    waveform["ti"]["central"] = [np.NaN] * self.commonTimeLength

            waveform["ne"]["central"] = self.connection.partial_get(
                "core_profiles", "profiles_1d(:)/electrons/density(0)"
            )
            waveform["zeff"]["central"] = self.connection.partial_get("core_profiles", "profiles_1d(:)/zeff(0)")

            waveform["n_species"] = {}
            waveform["ni"] = self.createWaveForm(self.commonTimeLength)
            for ispecies in range(self.nspeciesCore):
                if self.isCompositionAvailable and (
                    self.nspec_over_ne[ispecies] > KineticProfilesCompute.IMPURITY_LIMIT
                ):
                    waveform["n_species"][self.species[ispecies]] = {
                        "density": self.createWaveForm(0),
                        "vpol": self.createWaveForm(0),
                        "vtor": self.createWaveForm(0),
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
                        waveform["n_species"][self.species[ispecies]]["density"]["central"] = [
                            np.NaN
                        ] * self.commonTimeLength
                        waveform["n_species"][self.species[ispecies]]["vpol"]["central"] = [
                            np.NaN
                        ] * self.commonTimeLength
                        waveform["n_species"][self.species[ispecies]]["vtor"]["central"] = [
                            np.NaN
                        ] * self.commonTimeLength

                    for itime in range(self.commonTimeLength):
                        waveform["ni"]["central"][itime] = (
                            waveform["ni"]["central"][itime]
                            + waveform["n_species"][self.species[ispecies]]["density"]["central"][itime]
                        )
            return waveform
        return None
