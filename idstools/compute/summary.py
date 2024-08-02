"""
This module provides compute functions and classes for summary ids data

`more about summary ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/latest.html>`_.

"""

import logging

import numpy as np
from imas import imasdef

logger = logging.getLogger("module")


class SummaryCompute:
    """This class provides compute functions for summary ids"""

    def __init__(self, ids):
        """Initialization SummaryCompute object.

        Args:
            ids : summary ids object
        """
        self.ids = ids

    def get_summary(
        self,
    ):
        """
        The function `get_summary` processes and retrieves various waveforms and power values, handling
        missing data and logging critical errors when necessary.

        Returns:
            The `get_summary` method returns a dictionary named `waveform` containing various waveforms
        and their values. The waveforms included in the dictionary are "time", "ip",
        "current_non_inductive", "current_bootstrap", "v_loop", "beta_tor_norm", "beta_pol",
        "energy_diamagnetic", "energy_mhd", "current_ohm", "energy_total
        """
        stime = len(self.ids.time)
        # Ip waveform
        if len(self.ids.global_quantities.ip.value) < 1:
            logger.critical("summary.global_quantities.ip.value could not be read")
            self.ids.global_quantities.ip.value = np.asarray([np.nan] * stime)

        # Current_non_inductive waveform
        if len(self.ids.global_quantities.current_non_inductive.value) < 1:
            logger.critical("summary.global_quantities.current_non_inductive.value could not be read")
            self.ids.global_quantities.current_non_inductive.value = np.asarray([np.nan] * stime)

        # Current_bootstrap waveform
        if len(self.ids.global_quantities.current_bootstrap.value) < 1:
            logger.critical("summary.global_quantities.current_bootstrap.value could not be read")
            self.ids.global_quantities.current_bootstrap.value = np.asarray([np.nan] * stime)

        # V_loop waveform
        if len(self.ids.global_quantities.v_loop.value) < 1:
            logger.critical("summary.global_quantities.v_loop.value could not be read")
            self.ids.global_quantities.v_loop.value = np.asarray([np.nan] * stime)

        # Beta_tor_norm waveform
        if len(self.ids.global_quantities.beta_tor_norm.value) < 1:
            logger.critical("summary.global_quantities.beta_tor_norm.value could not be read")
            self.ids.global_quantities.beta_tor_norm.value = np.asarray([np.nan] * stime)

        # Beta_pol waveform
        if len(self.ids.global_quantities.beta_pol.value) < 1:
            logger.critical("summary.global_quantities.beta_pol.value could not be read")
            self.ids.global_quantities.beta_pol.value = np.asarray([np.nan] * stime)

        # Energy_diamagnetic waveform
        if len(self.ids.global_quantities.energy_diamagnetic.value) < 1:
            logger.critical("summary.global_quantities.energy_diamagnetic.value could not be read")
            self.ids.global_quantities.energy_diamagnetic.value = np.asarray([np.nan] * stime)

        # Energy_mhd waveform
        if len(self.ids.global_quantities.energy_mhd.value) < 1:
            logger.critical("summary.global_quantities.energy_mhd.value could not be read")
            self.ids.global_quantities.energy_mhd.value = np.asarray([np.nan] * stime)

        # Current_ohm waveform
        if len(self.ids.global_quantities.current_ohm.value) < 1:
            logger.critical("summary.global_quantities.current_ohm.value could not be read")
            self.ids.global_quantities.current_ohm.value = np.asarray([np.nan] * stime)

        # Energy_total waveform
        if len(self.ids.global_quantities.energy_total.value) < 1:
            logger.critical("summary.global_quantities.energy_total.value could not be read")
            self.ids.global_quantities.energy_total.value = np.asarray([np.nan] * stime)

        # Energy_thermal waveform
        if len(self.ids.global_quantities.energy_thermal.value) < 1:
            logger.critical("summary.global_quantities.energy_thermal.value could not be read")
            self.ids.global_quantities.energy_thermal.value = np.asarray([np.nan] * stime)

        # B0 waveform
        if len(self.ids.global_quantities.b0.value) < 1:
            logger.critical("summary.global_quantities.b0.value could not be read")
            self.ids.global_quantities.b0.value = np.asarray([np.nan] * stime)

        # H_98 waveform
        if len(self.ids.global_quantities.h_98.value) < 1:
            logger.critical("summary.global_quantities.h_98.value could not be read")
            self.ids.global_quantities.h_98.value = np.asarray([np.nan] * stime)

        # Tau_energy waveform
        if len(self.ids.global_quantities.tau_energy.value) < 1:
            logger.critical("summary.global_quantities.tau_energy.value could not be read")
            self.ids.global_quantities.tau_energy.value = np.asarray([np.nan] * stime)

        # H-mode flag
        if len(self.ids.global_quantities.h_mode.value) < 1:
            logger.critical("summary.global_quantities.h_mode.value could not be read")
            self.ids.global_quantities.h_mode.value = np.asarray([np.nan] * stime)

        # ----------------------------------------------------------------------

        # H&CD power
        p_ec = np.asarray([0.0] * stime)
        p_ic = np.asarray([0.0] * stime)
        p_nbi = np.asarray([0.0] * stime)
        p_lh = np.asarray([0.0] * stime)
        n_ec = len(self.ids.heating_current_drive.ec)
        n_ic = len(self.ids.heating_current_drive.ic)
        n_nbi = len(self.ids.heating_current_drive.nbi)
        n_lh = len(self.ids.heating_current_drive.lh)
        if n_ec > 0:
            for isource in range(n_ec):
                if len(self.ids.heating_current_drive.ec[isource].power.value) > 0:
                    p_ec = p_ec + self.ids.heating_current_drive.ec[isource].power.value
        else:
            if len(self.ids.heating_current_drive.power_ec.value) > 0:
                p_ec = self.ids.heating_current_drive.power_ec.value

        if n_ic > 0:
            for isource in range(n_ic):
                if len(self.ids.heating_current_drive.ic[isource].power.value) > 0:
                    p_ic = p_ic + self.ids.heating_current_drive.ic[isource].power.value
        else:
            if len(self.ids.heating_current_drive.power_ic.value) > 0:
                p_ic = self.ids.heating_current_drive.power_ic.value

        if n_nbi > 0:
            for isource in range(n_nbi):
                if len(self.ids.heating_current_drive.nbi[isource].power.value) > 0:
                    p_nbi = p_nbi + self.ids.heating_current_drive.nbi[isource].power.value
        else:
            if len(self.ids.heating_current_drive.power_nbi.value) > 0:
                p_nbi = self.ids.heating_current_drive.power_nbi.value

        if n_lh > 0:
            for isource in range(n_lh):
                if len(self.ids.heating_current_drive.lh[isource].power.value) > 0:
                    p_lh = p_lh + self.ids.heating_current_drive.lh[isource].power.value
        else:
            if len(self.ids.heating_current_drive.power_lh.value) > 0:
                p_nbi = self.ids.heating_current_drive.power_lh.value

        p_hcd = p_ec + p_ic + p_nbi + p_lh

        if sum(p_hcd) == 0 and sum(self.ids.heating_current_drive.power_additional.value) != 0:
            p_hcd = self.ids.heating_current_drive.power_additional.value

        # Fusion power
        p_fus = np.asarray([0.0] * stime)
        if len(self.ids.fusion.power.value) > 0:
            p_fus = self.ids.fusion.power.value

        # Ohmic power
        p_ohmic = np.asarray([0.0] * stime)
        if len(self.ids.global_quantities.power_ohm.value) > 0:
            p_ohmic = self.ids.global_quantities.power_ohm.value

        # Steady power
        p_steady = np.asarray([0.0] * stime)
        if len(self.ids.global_quantities.power_steady.value) > 0:
            p_steady = self.ids.global_quantities.power_steady.value

        # Neutron power
        p_neut = np.asarray([0.0] * stime)
        if len(self.ids.fusion.neutron_power_total.value) > 0:
            p_neut = self.ids.fusion.neutron_power_total.value

        # H-mode flag

        # Create the dictionary defining the list of waveforms (central values) that can be displayed
        waveform = {}
        waveform["time"] = self.ids.time  # timevec
        waveform["ip"] = self.ids.global_quantities.ip.value
        waveform["current_non_inductive"] = self.ids.global_quantities.current_non_inductive.value
        waveform["current_bootstrap"] = self.ids.global_quantities.current_bootstrap.value
        waveform["v_loop"] = self.ids.global_quantities.v_loop.value
        waveform["beta_tor_norm"] = self.ids.global_quantities.beta_tor_norm.value
        waveform["beta_pol"] = self.ids.global_quantities.beta_pol.value
        waveform["energy_diamagnetic"] = self.ids.global_quantities.energy_diamagnetic.value
        waveform["energy_mhd"] = self.ids.global_quantities.energy_mhd.value
        waveform["current_ohm"] = self.ids.global_quantities.current_ohm.value
        waveform["energy_total"] = self.ids.global_quantities.energy_total.value
        waveform["energy_thermal"] = self.ids.global_quantities.energy_thermal.value
        waveform["b0"] = self.ids.global_quantities.b0.value
        waveform["h_98"] = self.ids.global_quantities.h_98.value

        for t in range(len(waveform["h_98"])):
            if waveform["h_98"][t] < 0:
                waveform["h_98"][t] = 0

        waveform["tau_energy"] = self.ids.global_quantities.tau_energy.value
        waveform["h_mode"] = self.ids.global_quantities.h_mode.value.astype(float)
        waveform["p_hcd"] = p_hcd
        waveform["p_ec"] = p_ec
        waveform["p_ic"] = p_ic
        waveform["p_nbi"] = p_nbi
        waveform["p_lh"] = p_lh
        waveform["p_fusion"] = p_fus
        waveform["p_neutron"] = p_neut
        waveform["p_ohmic"] = p_ohmic
        waveform["p_steady"] = p_steady
        for k in waveform.keys():
            waveform[k][waveform[k] == imasdef.EMPTY_DOUBLE] = np.nan

        return waveform

    def get_h_mode_info(self):
        """
        The function `getHModeInfo` checks if the `h_mode` values are present in the `global_quantities`
        and returns information about the presence of HMode, as well as the minimum and maximum time
        values where HMode is present.

        Returns:
            a dictionary with three keys: "HModePresent", "th_min", and "th_max". The values associated
            with these keys are the boolean value indicating whether HMode is present, the minimum value
            of time when HMode is present, and the maximum value of time when HMode is present, respectively.
        """
        stime = len(self.ids.time)
        if len(self.ids.global_quantities.h_mode.value) < 1:
            logger.critical("summary.global_quantities.h_mode.value could not be read")
            self.ids.global_quantities.h_mode.value = np.asarray([np.nan] * stime)

        h_mode = self.ids.global_quantities.h_mode.value.astype(float)
        th_min = None
        th_max = None
        if np.size(h_mode[2:]) > 2:

            def indices(a, func):
                return [i for (i, val) in enumerate(a) if func(val)]

            h_mode_indices = indices(h_mode[2:], lambda h_mode_flag: h_mode_flag > 0)
            if len(h_mode_indices) > 0:
                h_mode_present = True
                th_min = self.ids.time[h_mode_indices[0]]
                th_max = self.ids.time[h_mode_indices[-1]]
            else:
                h_mode_present = False
        else:
            h_mode_present = False
        return {"h_mode_present": h_mode_present, "th_min": th_min, "th_max": th_max}
