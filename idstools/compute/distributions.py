"""
This module provides compute functions and classes for distributions ids data

"""

import logging


logger = logging.getLogger("module")


class DistributionsCompute:
    def __init__(self, ids):
        self.ids = ids

        # calculations
        self.ndistributions = len(self.ids.distribution)

        self.nrho = None
        self.rho_tor_norm = None
        self.cur_calc = None
        self.activeDistributions = None
        self.radialGridInfo = None
        self.isRadialGridInfoProcessed = False

    def getRadialGridInfo(self, timeIndex=0):
        radialGridInfo = {}
        for idistrib in range(self.ndistributions):
            distributionsData = {}
            distributionsData["is_active"] = 0
            distributionsData["cur_calc"] = 1
            distributionsData["nrho"] = 0
            distributionsData["rho_tor_norm"] = None
            if len(self.ids.distribution[idistrib].global_quantities[0].collisions.ion) > 0:
                distributionsData["is_active"] = 1
                if self.ids.distribution[idistrib].global_quantities[0].current_tor == -9e40:
                    distributionsData["cur_calc"] = 0
                try:
                    distributionsData["rho_tor_norm"] = 0
                    if len(self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor_norm) > 0:
                        distributionsData["nrho"] = len(
                            self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor_norm
                        )
                        distributionsData["rho_tor_norm"] = (
                            self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor_norm
                        )
                    elif len(self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor) > 0:
                        distributionsData["nrho"] = len(
                            self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor
                        )
                        distributionsData["rho_tor_norm"] = (
                            self.ids.distribution[idistrib].profiles_1d[timeIndex].grid.rho_tor
                            / self.ids.distribution[idistrib]
                            .profiles_1d[timeIndex]
                            .grid.rho_tor[distributionsData["nrho"] - 1]
                        )
                except Exception as e:
                    logger.warning(
                        "distributions.distribution[idistrib].profiles_1d[it].grid.rho_tor_norm and"
                        "rho_tor could not be read"
                    )
                    logger.debug(f"{e}")
                    return None
                if distributionsData["nrho"] == 0:
                    logger.warning(
                        "distributions.distribution[idistrib].profiles_1d[it].grid.rho_tor_norm and rho_tor are empty"
                    )
                    return None

            radialGridInfo[idistrib] = distributionsData
        self.activeDistributions = {key: value for key, value in radialGridInfo.items() if value["is_active"] == 1}
        if not radialGridInfo:
            return None
        self.nrho = radialGridInfo[0]["nrho"]
        self.rho_tor_norm = radialGridInfo[0]["rho_tor_norm"]
        self.cur_calc = radialGridInfo[0]["cur_calc"]
        self.radialGridInfo = radialGridInfo
        self.isRadialGridInfoProcessed = True
        return radialGridInfo

    def getProfiles(self, timeIndex=0):
        if self.nrho is None:
            return None
        timeArray = self.ids.time
        ntime = len(timeArray)
        if self.isRadialGridInfoProcessed is False:
            self.getRadialGridInfo(timeIndex)
        profiles = {}
        # INJECTOR NAME
        profiles["single_nf_source_name"] = dict()

        # WAVEFORMS
        profiles["all_injectors_current_waveform"] = [0] * ntime
        profiles["all_injectors_electron_power_waveform"] = [0] * ntime
        profiles["all_injectors_ion_power_waveform"] = [0] * ntime
        profiles["all_injectors_total_power_waveform"] = [0] * ntime
        profiles["single_current_waveform"] = dict()
        profiles["single_electron_power_waveform"] = dict()
        profiles["single_ion_power_waveform"] = dict()
        profiles["single_total_power_waveform"] = dict()

        # PROFILES
        profiles["all_injectors_current_density_profile"] = [0] * self.nrho
        profiles["all_injectors_electron_power_density_profile"] = [0] * self.nrho
        profiles["all_injectors_ion_power_density_profile"] = [0] * self.nrho
        profiles["all_injectors_total_power_density_profile"] = [0] * self.nrho
        profiles["single_current_density_profile"] = dict()
        profiles["single_electron_power_density_profile"] = dict()
        profiles["single_ion_power_density_profile"] = dict()
        profiles["single_total_power_density_profile"] = dict()

        # LOOP OVER ALL SOURCE
        for idistrib in range(self.ndistributions):
            # INJECTOR NAME
            if len(self.ids.distribution[idistrib].process) > 0:
                if len(self.ids.distribution[idistrib].process[0].type.description) > 0:
                    profiles["single_nf_source_name"][idistrib] = self.ids.distribution[idistrib].process[
                        0
                    ].type.description + str(idistrib)
                else:
                    profiles["single_nf_source_name"][idistrib] = f"Beam_f{idistrib}"
            else:
                profiles["single_nf_source_name"][idistrib] = f"Beam_{idistrib}"
            if self.radialGridInfo[idistrib]["is_active"]:
                # WAVEFORMS
                profiles["single_current_waveform"][idistrib] = [0] * ntime
                profiles["single_electron_power_waveform"][idistrib] = [0] * ntime
                profiles["single_ion_power_waveform"][idistrib] = [0] * ntime
                profiles["single_total_power_waveform"][idistrib] = [0] * ntime
                nions = len(self.ids.distribution[idistrib].global_quantities[0].collisions.ion)
                for itime in range(ntime):
                    if self.cur_calc == 1:
                        profiles["single_current_waveform"][idistrib][itime] = (
                            self.ids.distribution[idistrib].global_quantities[itime].current_tor
                        )
                    profiles["single_electron_power_waveform"][idistrib][itime] = (
                        self.ids.distribution[idistrib].global_quantities[itime].collisions.electrons.power_thermal
                    )
                    for iion in range(nions):
                        profiles["single_ion_power_waveform"][idistrib][itime] = (
                            profiles["single_ion_power_waveform"][idistrib][itime]
                            + self.ids.distribution[idistrib]
                            .global_quantities[itime]
                            .collisions.ion[iion]
                            .power_thermal
                        )
                    profiles["single_total_power_waveform"][idistrib][itime] = (
                        profiles["single_electron_power_waveform"][idistrib][itime]
                        + profiles["single_ion_power_waveform"][idistrib][itime]
                    )
                    profiles["all_injectors_current_waveform"][itime] = (
                        profiles["all_injectors_current_waveform"][itime]
                        + profiles["single_current_waveform"][idistrib][itime]
                    )
                    profiles["all_injectors_electron_power_waveform"][itime] = (
                        profiles["all_injectors_electron_power_waveform"][itime]
                        + profiles["single_electron_power_waveform"][idistrib][itime]
                    )
                    profiles["all_injectors_ion_power_waveform"][itime] = (
                        profiles["all_injectors_ion_power_waveform"][itime]
                        + profiles["single_ion_power_waveform"][idistrib][itime]
                    )
                    profiles["all_injectors_total_power_waveform"][itime] = (
                        profiles["all_injectors_total_power_waveform"][itime]
                        + profiles["single_electron_power_waveform"][idistrib][itime]
                        + profiles["single_ion_power_waveform"][idistrib][itime]
                    )
                # PROFILES
                profiles["single_current_density_profile"][idistrib] = [0] * self.nrho
                profiles["single_electron_power_density_profile"][idistrib] = [0] * self.nrho
                profiles["single_ion_power_density_profile"][idistrib] = [0] * self.nrho
                profiles["single_total_power_density_profile"][idistrib] = [0] * self.nrho
                if self.cur_calc == 1:
                    profiles["single_current_density_profile"][idistrib] = (
                        self.ids.distribution[idistrib].profiles_1d[timeIndex].current_tor
                    )
                profiles["single_electron_power_density_profile"][idistrib] = (
                    self.ids.distribution[idistrib].profiles_1d[timeIndex].collisions.electrons.power_thermal
                )
                for iion in range(nions):
                    profiles["single_ion_power_density_profile"][idistrib] = (
                        profiles["single_ion_power_density_profile"][idistrib]
                        + self.ids.distribution[idistrib].profiles_1d[timeIndex].collisions.ion[iion].power_thermal
                    )
                profiles["single_total_power_density_profile"][idistrib] = (
                    profiles["single_electron_power_density_profile"][idistrib]
                    + profiles["single_ion_power_density_profile"][idistrib]
                )
                profiles["all_injectors_current_density_profile"] = (
                    profiles["all_injectors_current_density_profile"]
                    + profiles["single_current_density_profile"][idistrib]
                )
                profiles["all_injectors_electron_power_density_profile"] = (
                    profiles["all_injectors_electron_power_density_profile"]
                    + profiles["single_electron_power_density_profile"][idistrib]
                )
                profiles["all_injectors_ion_power_density_profile"] = (
                    profiles["all_injectors_ion_power_density_profile"]
                    + profiles["single_ion_power_density_profile"][idistrib]
                )
                profiles["all_injectors_total_power_density_profile"] = (
                    profiles["all_injectors_total_power_density_profile"]
                    + profiles["single_electron_power_density_profile"][idistrib]
                    + profiles["single_ion_power_density_profile"][idistrib]
                )

        logger.info(
            " Total power  = {:.2f}".format(profiles["all_injectors_total_power_waveform"][timeIndex] * 1.0e-6) + " MW"
        )
        logger.info(
            " To electrons = {:.2f}".format(profiles["all_injectors_electron_power_waveform"][timeIndex] * 1.0e-6)
            + " MW"
        )
        logger.info(
            " To ions      = {:.2f}".format(profiles["all_injectors_ion_power_waveform"][timeIndex] * 1.0e-6) + " MW"
        )

        if self.cur_calc == 1:
            logger.info(
                " Total CD        = {:.2f}".format(profiles["all_injectors_current_waveform"][timeIndex] * 1.0e-3)
                + " kA"
            )

        if len(self.activeDistributions) != 0:
            for idistrib in range(self.ndistributions):
                if self.radialGridInfo[idistrib]["is_active"]:
                    logger.info(
                        " Distribution #"
                        + str(idistrib + 1)
                        + " - power = {:.2f}".format(
                            profiles["single_total_power_waveform"][idistrib][timeIndex] * 1.0e-6
                        )
                        + " MW"
                    )
                    if self.cur_calc == 1:
                        logger.info(
                            " Distribution #"
                            + str(idistrib + 1)
                            + " - CD    = {:.2f}".format(
                                profiles["single_current_waveform"][idistrib][timeIndex] * 1.0e-3
                            )
                            + " kA"
                        )
        return profiles

    def getPowerAbsorbedtoIndividualIons(self, timeIndex, verbose=False):
        if self.isRadialGridInfoProcessed is False:
            self.getRadialGridInfo(timeIndex)
        import idstools.init_mendeleiev as mend

        table_mendeleiev = mend.create_table_mendeleiev()
        powerAbsorbed = {}

        nions = len(self.ids.distribution[0].global_quantities[0].collisions.ion)
        # Power absorbed to individual ions
        powerAbsorbed["all_injectors_total_power_waveform_per_ion"] = [0] * nions
        powerAbsorbed["element"] = [0] * nions
        powerAbsorbed["compo_detail"] = 0
        for distribIndex in range(self.ndistributions):
            nions = len(self.ids.distribution[distribIndex].global_quantities[0].collisions.ion)
            if self.radialGridInfo[distribIndex]["is_active"]:
                for ionIndex in range(nions):
                    powerAbsorbed["all_injectors_total_power_waveform_per_ion"][ionIndex] = (
                        powerAbsorbed["all_injectors_total_power_waveform_per_ion"][ionIndex]
                        + self.ids.distribution[distribIndex]
                        .global_quantities[timeIndex]
                        .collisions.ion[ionIndex]
                        .power_thermal
                    )
                    if (
                        len(
                            self.ids.distribution[distribIndex]
                            .global_quantities[timeIndex]
                            .collisions.ion[ionIndex]
                            .element
                        )
                        > 0
                    ):
                        powerAbsorbed["compo_detail"] = 1
                        a = int(
                            self.ids.distribution[distribIndex]
                            .global_quantities[timeIndex]
                            .collisions.ion[ionIndex]
                            .element[0]
                            .a
                        )
                        z = int(
                            self.ids.distribution[distribIndex]
                            .global_quantities[timeIndex]
                            .collisions.ion[ionIndex]
                            .element[0]
                            .z_n
                        )
                        powerAbsorbed["element"][ionIndex] = table_mendeleiev[z][a].element
                        logger.info(
                            "      - "
                            + z["element"][ionIndex]
                            + " = {:.2f}".format(z["all_injectors_total_power_waveform_per_ion"][ionIndex] * 1.0e-3)
                            + " kW"
                        )

        return powerAbsorbed
