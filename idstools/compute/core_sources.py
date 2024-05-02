""" 
This module provides compute functions and classes for core_sources ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""
import logging
import numpy as np
import functools
from typing import Dict

logger = logging.getLogger("module")


class CoreSourcesCompute:
    def __init__(self, ids):
        self.ids = ids

    def getFluxInfoFromSources(self):
        """
        The `getFluxInfoFromSources` function retrieves information about sources, including their name, particle flux, energy flux, and ion properties, and returns a dictionary containing this information.

        Returns:
            The function `getFluxInfoFromSources` returns a dictionary containing
            information about the sources. The dictionary has the following
            structure: 
            
            .. code-block:: python
            
                {
                    0: {
                        "energy_flux": 22081836.173650958,
                        "ions": {
                            0: {
                                "a": 2.0,
                                "energy_flux": None,
                                "particles_flux": 4.947616643196025e21,
                                "z_ion": -9e40,
                                "z_n": 1.0,
                            },
                            "name": "total",
                            "particles_flux": None,
                        },
                    }
                }
        """
        sourcesDict = {}
        for sourceIndex, source in enumerate(self.ids.source):
            sourceDict = {
                "name": source.identifier.name,
                "particles_flux": None,
                "energy_flux": None,
                "ions": {},
            }
            if (len(source.profiles_1d)) != 0:
                if len(source.profiles_1d[0].electrons.particles) != 0:
                    gridVolume = (
                        np.asarray(
                            [np.nan] * len(source.profiles_1d[0].electrons.particles)
                        )
                        if len(source.profiles_1d[0].grid.volume) == 0
                        else source.profiles_1d[0].grid.volume
                    )
                    sourceDict["particles_flux"] = np.trapz(
                        source.profiles_1d[0].electrons.particles,
                        gridVolume,
                    )
                if len(source.profiles_1d[0].electrons.energy) != 0:
                    gridVolume = (
                        np.asarray(
                            [np.nan] * len(source.profiles_1d[0].electrons.energy)
                        )
                        if len(source.profiles_1d[0].grid.volume) == 0
                        else source.profiles_1d[0].grid.volume
                    )
                    sourceDict["energy_flux"] = np.trapz(
                        source.profiles_1d[0].electrons.energy,
                        gridVolume,
                    )
                ionsDict = {}
                for ionIndex, ion in enumerate(source.profiles_1d[0].ion):
                    ionDict = {
                        "a": ion.element[0].a,
                        "z_n": ion.element[0].z_n,
                        "z_ion": ion.z_ion,
                    }
                    if len(ion.particles) != 0:
                        ionDict["particles_flux"] = np.trapz(
                            ion.particles, source.profiles_1d[0].grid.volume
                        )
                    else:
                        ionDict["particles_flux"] = None
                    if len(ion.energy) != 0:
                        ionDict["energy_flux"] = np.trapz(
                            ion.energy, source.profiles_1d[0].grid.volume
                        )
                    else:
                        ionDict["energy_flux"] = None
                    ionsDict[ionIndex] = ionDict
                sourceDict["ions"] = ionsDict
            sourcesDict[sourceIndex] = sourceDict
        return sourcesDict

    @functools.lru_cache(maxsize=128)
    def getRhoTorNorm(self) -> np.ndarray:
        """
        The function `getRhoTorNorm` returns the value of `grid.rho_tor_norm` if it is not empty, otherwise it returns None.

        Returns:
            the value of the variable `rhoTorNorm`.
        """
        if len(self.ids.source) == 0:
            return None
        rhoTorNorm = None
        try:
            if len(self.ids.source[0].profiles_1d[0].grid.rho_tor_norm) > 0:
                rhoTorNorm = self.ids.source[0].profiles_1d[0].grid.rho_tor_norm
            elif len(self.ids.source[0].profiles_1d[0].grid.rho_tor) > 0:
                nrho = len(self.ids.source[0].profiles_1d[0].grid.rho_tor)
                rhoTorNorm = (
                    self.ids.source[0].profiles_1d[0].grid.rho_tor
                    / self.ids.source[0].profiles_1d[0].grid.rho_tor[nrho - 1]
                )
        except Exception:
            logger.critical(
                "core_sources.source[isource].profiles_1d[0].grid.rho_tor_norm and rho_tor could not be read"
            )
            return None
        if rhoTorNorm is not None and len(rhoTorNorm) == 0:
            logger.critical(
                "core_sources.source[isource].profiles_1d[0].grid.rho_tor_norm and rho_tor are empty"
            )
            return None
        return rhoTorNorm

    @functools.lru_cache(maxsize=128)
    def getValidAndActiveSources(self) -> Dict[int, Dict[str, bool]]:
        """
        The function `getValidAndActiveSources` returns a dictionary of valid and active sources, where each source is represented by a dictionary with the keys "valid" and "active".

        Returns:
            a dictionary of dictionaries. The outer dictionary has integer keys representing the index of each source, and the inner dictionaries have string keys ("valid" and "active") representing the validity and activity status of each source.
        """
        sources = {}
        for sourceIndex, sourceInfo in enumerate(self.ids.source):
            source = {}
            if len(sourceInfo.global_quantities) > 0:
                source["valid"] = True
                source["active"] = (
                    True if sourceInfo.global_quantities[0].power > 0 else False
                )
            else:
                source["valid"] = False
                source["active"] = False
                logger.critical(
                    f"core_sources.source[{sourceIndex}] has no global_quantities, will be discarded."
                )
            sources[sourceIndex] = source
        return sources

    @functools.lru_cache(maxsize=128)
    def isActiveSourceAvailable(self) -> bool:
        """
        The function checks if there is an active source available among the valid and active sources.

        Returns:
            a boolean value. It is checking if there are any active sources in the list of valid and active sources and returning True if there is at least one active source, and False otherwise.
        """
        sources = self.getValidAndActiveSources()
        return any(source["active"] for _, source in sources.items())

    def getSourceNames(self) -> Dict:
        sources = self.getValidAndActiveSources()
        single_source_name = {}
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                single_source_name[sourceIndex] = self.ids.source[
                    sourceIndex
                ].identifier.name.upper()
        return single_source_name

    @functools.lru_cache(maxsize=128)
    def getSingleAndTotalElectronsAndIonsProfiles(self) -> Dict[str, np.ndarray]:
        """
        The function `getSingleAndTotalElectronsAndIonsProfiles` returns the total current profile and the individual current profiles for each valid and active source.
        SINGLE AND TOTAL PROFILES (ELECTRONS+IONS)
        Returns:
            a dictionary with two keys: "totalCurrentProfile" and "singleCurrentProfile". The value associated with the "totalCurrentProfile" key is a numpy array representing the total current profile. The value associated with the "singleCurrentProfile" key is a dictionary where the keys are the indices of the sources and the values are numpy arrays representing the current profiles for each individual source.
        """
        # SINGLE AND TOTAL PROFILES (ELECTRONS+IONS)
        # total_power_profile                = [0]*nrho  # profile
        # total_particles_profile            = [0]*nrho  # profile
        # single_power_profile               = dict()    # profile
        # single_particles_profile           = dict()    # profile
        nrho = len(self.getRhoTorNorm())
        totalCurrentProfile = np.zeros(nrho)
        singleCurrentProfile = {}
        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():  # range(nsources):
            if source["valid"] == True and source["active"] == True:
                if len(self.ids.source[sourceIndex].profiles_1d[0].j_parallel) > 0:
                    totalCurrentProfile = (
                        totalCurrentProfile
                        + self.ids.source[sourceIndex].profiles_1d[0].j_parallel
                    )
                    singleCurrentProfile[sourceIndex] = (
                        self.ids.source[sourceIndex].profiles_1d[0].j_parallel
                    )
                else:
                    singleCurrentProfile[sourceIndex] = np.zeros(nrho)
        return {
            "totalCurrentProfile": totalCurrentProfile,
            "singleCurrentProfile": singleCurrentProfile,
        }

    @functools.lru_cache(maxsize=128)
    def getSingleAndTotalElectronsProfiles(self) -> Dict[str, np.ndarray]:
        """
        The function `getSingleAndTotalElectronsProfiles` calculates and returns profiles of total  electron power, total electron particles, single electron power, and single electron particles.

        Returns:
            a dictionary with the following keys and values: totalElectronPowerProfile, totalElectronParticlesProfile, singleElectronPowerProfile, singleElectronParticlesProfile,
        """
        # SINGLE AND TOTAL PROFILES (ELECTRONS)
        # totalElectronPowerProfile       = [0]*nrho  # profile
        # total_electron_particles_profile   = [0]*nrho  # profile
        # single_electron_power_profile      = dict()    # profile
        # single_electron_particles_profile  = dict()    # profile
        nrho = len(self.getRhoTorNorm())
        totalElectronPowerProfile = np.zeros(nrho)
        totalElectronParticlesProfile = np.zeros(nrho)
        singleElectronPowerProfile = {}
        singleElectronParticlesProfile = {}

        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                if (
                    len(self.ids.source[sourceIndex].profiles_1d[0].electrons.energy)
                    < 1
                ):
                    self.ids.source[sourceIndex].profiles_1d[
                        0
                    ].electrons.energy = np.zeros(nrho)
                if (
                    len(self.ids.source[sourceIndex].profiles_1d[0].electrons.particles)
                    < 1
                ):
                    self.ids.source[sourceIndex].profiles_1d[
                        0
                    ].electrons.particles = np.zeros(nrho)

                totalElectronPowerProfile = (
                    totalElectronPowerProfile
                    + self.ids.source[sourceIndex].profiles_1d[0].electrons.energy
                )
                totalElectronParticlesProfile = (
                    totalElectronParticlesProfile
                    + self.ids.source[sourceIndex].profiles_1d[0].electrons.particles
                )

                singleElectronPowerProfile[sourceIndex] = (
                    self.ids.source[sourceIndex].profiles_1d[0].electrons.energy
                )
                singleElectronParticlesProfile[sourceIndex] = (
                    self.ids.source[sourceIndex].profiles_1d[0].electrons.particles
                )

        return {
            "totalElectronPowerProfile": totalElectronPowerProfile,
            "totalElectronParticlesProfile": totalElectronParticlesProfile,
            "singleElectronPowerProfile": singleElectronPowerProfile,
            "singleElectronParticlesProfile": singleElectronParticlesProfile,
        }

    def getSingleAndTotalIonProfiles(self) -> Dict[str, np.ndarray]:
        """
        The function `getSingleAndTotalIonProfiles` calculates the total and individual power and particle profiles for ions in a plasma simulation.

        Returns:
            a dictionary with the following keys and values:totalIonPowerProfile, totalIonParticlesProfile, singleIonPowerProfile, singleIonParticlesProfile
        """
        # SINGLE AND TOTAL PROFILES (IONS)
        # total_ion_power_profile = [0] * nrho  # profile
        # total_ion_particles_profile = [0] * nrho  # profile
        # single_ion_power_profile = dict()  # profile
        # single_ion_particles_profile = dict()  # profile
        nrho = len(self.getRhoTorNorm())
        totalIonPowerProfile = np.zeros(nrho)
        totalIonParticlesProfile = np.zeros(nrho)
        singleIonPowerProfile = {}
        singleIonParticlesProfile = {}

        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                singleIonPowerProfile[sourceIndex] = np.zeros(nrho)
                singleIonParticlesProfile[sourceIndex] = np.zeros(nrho)
                for ion in self.ids.source[sourceIndex].profiles_1d[0].ion:
                    if len(ion.energy) < 1:
                        ion.energy = [0] * nrho
                    if len(ion.particles) < 1:
                        ion.particles = [0] * nrho

                    singleIonPowerProfile[sourceIndex] = (
                        singleIonPowerProfile[sourceIndex] + ion.energy
                    )
                    singleIonParticlesProfile[sourceIndex] = (
                        singleIonParticlesProfile[sourceIndex] + ion.particles
                    )

                    totalIonPowerProfile = totalIonPowerProfile + ion.energy
                    totalIonParticlesProfile = totalIonParticlesProfile + ion.particles
        return {
            "totalIonPowerProfile": totalIonPowerProfile,
            "totalIonParticlesProfile": totalIonParticlesProfile,
            "singleIonPowerProfile": singleIonPowerProfile,
            "singleIonParticlesProfile": singleIonParticlesProfile,
        }

    def getSingleAndTotalElectronsIonsWaveforms(
        self,
    ):
        # SINGLE AND TOTAL WAVEFORMS (ELECTRONS+IONS)
        # total_power_waveform = [0] * ntime  # waveform
        # total_particles_waveform = [0] * ntime  # waveform
        # single_power_waveform = dict()  # waveform
        # single_particles_waveform = dict()  # waveform
        timeLength = len(self.ids.time)
        total_power_waveform = np.zeros(timeLength)
        total_particles_waveform = np.zeros(timeLength)
        single_power_waveform = {}
        single_particles_waveform = {}
        dictSingleAndTotalElectronsWaveforms = (
            self.getSingleAndTotalElectronsWaveforms()
        )
        total_electron_power_waveform = dictSingleAndTotalElectronsWaveforms[
            "total_electron_power_waveform"
        ]
        total_electron_particles_waveform = dictSingleAndTotalElectronsWaveforms[
            "total_electron_particles_waveform"
        ]
        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                single_power_waveform[sourceIndex] = []
                single_particles_waveform[sourceIndex] = []
                for timeIndex in range(timeLength):
                    electrons_power = (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                    )
                    electrons_particles = (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                    )
                    total_ion_particles = (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_particles
                    )
                    total_ion_power = (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                    )

                    if electrons_power < 0:
                        electrons_power = 0.0
                    if electrons_particles < 0:
                        electrons_particles = 0.0
                    if total_ion_particles < 0:
                        total_ion_particles = 0.0
                    if total_ion_power < 0:
                        total_ion_power = 0.0

                    total_power_waveform[timeIndex] = (
                        total_electron_power_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                    )
                    total_particles_waveform[timeIndex] = (
                        total_electron_particles_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                    ) + self.ids.source[sourceIndex].global_quantities[
                        timeIndex
                    ].total_ion_particles
                    single_power_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                    )
                    single_particles_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_particles
                    )
                single_power_waveform[sourceIndex] = np.array(
                    single_power_waveform[sourceIndex]
                )
                single_particles_waveform[sourceIndex] = np.array(
                    single_particles_waveform[sourceIndex]
                )
        return {
            "total_power_waveform": total_power_waveform,
            "total_particles_waveform": total_particles_waveform,
            "single_power_waveform": single_power_waveform,
            "single_particles_waveform": single_particles_waveform,
        }

    def getSingleAndTotalElectronsWaveforms(self):
        """
        The function `getSingleAndTotalElectronsWaveforms` calculates and returns waveforms for total electron power, total electron particles, single electron power, and single electron particles.

        Returns:
            a dictionary with the following keys and values:
            "total_electron_power_waveform": total_electron_power_waveform,
            "total_electron_particles_waveform": total_electron_particles_waveform,
            "single_electron_power_waveform": single_electron_power_waveform,
            "single_electron_particles_waveform": single_electron_particles_waveform,
        """
        # SINGLE AND TOTAL WAVEFORMS (ELECTRONS)
        # total_electron_power_waveform = [0] * ntime  # waveform
        # total_electron_particles_waveform = [0] * ntime  # waveform
        # single_electron_power_waveform = dict()  # waveform
        # single_electron_particles_waveform = dict()  # waveform
        timeLength = len(self.ids.time)
        total_electron_power_waveform = np.zeros(timeLength)
        total_electron_particles_waveform = np.zeros(timeLength)
        single_electron_power_waveform = {}
        single_electron_particles_waveform = {}
        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                single_electron_power_waveform[sourceIndex] = []
                single_electron_particles_waveform[sourceIndex] = []
                for timeIndex in range(timeLength):
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                        < 0
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].electrons.power = 0.0
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                        < 0
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].electrons.particles = 0.0

                    total_electron_power_waveform[timeIndex] = (
                        total_electron_power_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                    )
                    total_electron_particles_waveform[timeIndex] = (
                        total_electron_particles_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                    )
                    single_electron_power_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.power
                    )
                    single_electron_particles_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .electrons.particles
                    )
                single_electron_power_waveform[sourceIndex] = np.array(
                    single_electron_power_waveform[sourceIndex]
                )
                single_electron_particles_waveform[sourceIndex] = np.array(
                    single_electron_particles_waveform[sourceIndex]
                )

        return {
            "total_electron_power_waveform": total_electron_power_waveform,
            "total_electron_particles_waveform": total_electron_particles_waveform,
            "single_electron_power_waveform": single_electron_power_waveform,
            "single_electron_particles_waveform": single_electron_particles_waveform,
        }

    def getSingleAndTotalIonsWaveforms(self):
        """
        The function `getSingleAndTotalIonsWaveforms` calculates and returns the waveforms for single ion power, single ion particles, total ion power, and total ion particles.

        Returns:
            a dictionary with four key-value pairs. The keys are "single_ion_power_waveform", "single_ion_particles_waveform", "total_ion_power_waveform", and "total_ion_particles_waveform". The corresponding values are the waveforms for single ion power, single ion particles, total ion power, and total ion particles, respectively.
        """
        # SINGLE AND TOTAL WAVEFORMS (IONS)
        # total_ion_power_waveform = [0] * ntime  # waveform
        # total_ion_particles_waveform = [0] * ntime  # waveform
        # single_ion_power_waveform = dict()  # waveform
        # single_ion_particles_waveform = dict()  # waveform
        timeLength = len(self.ids.time)
        total_ion_power_waveform = np.zeros(timeLength)  # waveform
        total_ion_particles_waveform = np.zeros(timeLength)  # waveform
        single_ion_power_waveform = {}  # waveform
        single_ion_particles_waveform = {}  # waveform
        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                single_ion_power_waveform[sourceIndex] = []
                single_ion_particles_waveform[sourceIndex] = []
                for timeIndex in range(timeLength):
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                        < 0
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].total_ion_power = 0.0
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_particles
                        < 0
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].total_ion_particles = 0.0
                    single_ion_power_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                    )
                    single_ion_particles_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_particles
                    )
                    total_ion_power_waveform[timeIndex] = (
                        total_ion_power_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_power
                    )
                    total_ion_particles_waveform[timeIndex] = (
                        total_ion_particles_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .total_ion_particles
                    )

                single_ion_power_waveform[sourceIndex] = np.array(
                    single_ion_power_waveform[sourceIndex]
                )
                single_ion_particles_waveform[sourceIndex] = np.array(
                    single_ion_particles_waveform[sourceIndex]
                )
        return {
            "single_ion_power_waveform": single_ion_power_waveform,
            "single_ion_particles_waveform": single_ion_particles_waveform,
            "total_ion_power_waveform": total_ion_power_waveform,
            "total_ion_particles_waveform": total_ion_particles_waveform,
        }

    def getSingleAndTotalCurrentTorque(self):
        """
        The function `getSingleAndTotalCurrentTorque` calculates the total and individual current and torque waveforms for a given set of sources.

        Returns:
            a dictionary with the following keys and values:
            "total_current_waveform": total_current_waveform,
            "total_torque_waveform": total_torque_waveform,
            "single_current_waveform": single_current_waveform,
            "single_torque_waveform": single_torque_waveform,
        """
        # SINGLE AND TOTAL CURRENT AND TORQUE
        # total_current_waveform = [0] * ntime  # waveform
        # total_torque_waveform = [0] * ntime  # waveform
        # single_current_waveform = dict()  # waveform
        # single_torque_waveform = dict()  # waveform

        timeLength = len(self.ids.time)

        total_current_waveform = np.zeros(timeLength)  # waveform
        total_torque_waveform = np.zeros(timeLength)  # waveform
        single_current_waveform = {}  # waveform
        single_torque_waveform = {}  # waveform

        sources = self.getValidAndActiveSources()
        for sourceIndex, source in sources.items():
            if source["valid"] == True and source["active"] == True:
                single_current_waveform[sourceIndex] = []
                single_torque_waveform[sourceIndex] = []
                for timeIndex in range(timeLength):
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .current_parallel
                        < -1.0e40
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].current_parallel = 0.0
                    if (
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .torque_tor
                        < 0
                    ):
                        self.ids.source[sourceIndex].global_quantities[
                            timeIndex
                        ].torque_tor = 0.0

                    total_current_waveform[timeIndex] = (
                        total_current_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .current_parallel
                    )
                    total_torque_waveform[timeIndex] = (
                        total_torque_waveform[timeIndex]
                        + self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .torque_tor
                    )
                    single_current_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .current_parallel
                    )
                    single_torque_waveform[sourceIndex].append(
                        self.ids.source[sourceIndex]
                        .global_quantities[timeIndex]
                        .torque_tor
                    )
                single_current_waveform[sourceIndex] = np.array(
                    single_current_waveform[sourceIndex]
                )
                single_torque_waveform[sourceIndex] = np.array(
                    single_torque_waveform[sourceIndex]
                )

        return {
            "total_current_waveform": total_current_waveform,
            "total_torque_waveform": total_torque_waveform,
            "single_current_waveform": single_current_waveform,
            "single_torque_waveform": single_torque_waveform,
        }
