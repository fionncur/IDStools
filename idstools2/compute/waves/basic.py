""" 
This module provides compute functions and classes for waves ids data

`more about waves ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/waves.html>`_.

"""

from typing import Any
import numpy as np
import sys
import functools


class WavesCompute:
    """This class provides compute functions for waves ids"""

    def __init__(self, ids):
        """Initialization WavesCompute object.

        Args:
            ids : waves ids object
        """
        self.ids = ids

    def getBResonance(
        self,
        coherentWaveIndex: int = 0,
        timeIndex: int = 0,
        harmonicFrequencies: list = None,
    ):
        """
        This function calculates the B-resonance (magnetic field) for a given coherent wave index, time index, and list of harmonic frequencies.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which we want to calculate the B resonance. Defaults to 0
            timeIndex (int): The index of the time step for which the bResonance is being calculated. Defaults to 0
            harmonicFrequencies (list): A list of integers representing the harmonic frequencies for which the B-resonance values are to be calculated. If this parameter is not provided, the function uses the default values of [1, 2, 3, 4].

        Returns:
            A list of values for the magnetic field resonance frequencies for the given coherent wave index, time index, and harmonic frequencies. The length of the list is equal to the length of the input harmonic frequencies list.


        Notes:
            .. math:: BResonance = \ 2*pi*ecfrequency*9.1e^-31/1.6e^-19/HarmonicFrequency

        Here harmonicFrequency is any value from [1,2,3,4]
        """
        if harmonicFrequencies is None:
            harmonicFrequencies = [1, 2, 3, 4]
        ecFrequency = (
            self.ids.coherent_wave[coherentWaveIndex]
            .global_quantities[timeIndex]
            .frequency
        )
        bResonance = [0] * len(harmonicFrequencies)
        for harmonicFrequencyIndex in range(len(harmonicFrequencies)):
            bResonance[harmonicFrequencyIndex] = (
                2
                * np.pi
                * ecFrequency
                * 9.1e-31
                / 1.6e-19
                / harmonicFrequencies[harmonicFrequencyIndex]
            )
        return bResonance

    def getBeamArray(self):
        """
        This function returns an array of beam indices based on the number of coherent waves.

        Returns:
            a numpy array of equally spaced values from 0 to nbeam-1, where nbeam is the length of the list `waves.coherent_wave`. This array represents the indices of the beams.
        """
        nBeam = len(self.ids.coherent_wave)
        return np.linspace(0, nBeam - 1, nBeam)

    def getOmegaEC(self, coherentWaveIndex: int = 0, timeIndex: int = 0) -> float:
        """
        This function returns the angular frequency of a coherent wave at a specific time index.

        Args:
            coherentWaveIndex (int): The index of the coherent wave for which the angular frequency needs to be calculated. Defaults to 0
            timeIndex (int): The time index parameter is used to specify the time step for which the frequency of the coherent wave is to be retrieved. Defaults to 0

        Returns:
            The value of the angular frequency (in radians per second) of a coherent wave at a specific time index. The value is calculated using the frequency of the coherent wave at the given time index and multiplying it by 2*pi.

        Notes:
            .. math:: OmegaEC = \ 2*pi*frequency

        """
        return (
            2
            * np.pi
            * self.ids.coherent_wave[coherentWaveIndex]
            .global_quantities[timeIndex]
            .frequency
        )

    @functools.lru_cache(maxsize=128)
    def getActiveBeams(self, beamTracingTimeIndex: int = 0):
        """
        This function returns a dictionary of active beams with their respective properties.

        Args:
            beamTracingTimeIndex (int): The parameter `beamTracingTimeIndex` is an integer that represents the index of the beam tracing time. Defaults to 0

        Returns:
            Dictionary called `activeBeams` which contains information about each beam in `waves.coherent_wave`. The dictionary has keys for each beam index and the values are  dictionaries containing the total number of beams and boolean indicating whether the beam is active or not. The function determines if a beam is active by checking if any of its rays have initial power greater than 0.
        """
        activeBeams = {}

        for beamIndex in range(len(self.ids.coherent_wave)):
            beamDict = {
                "total_beams": len(
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam
                ),
            }
            for rayIndex in range(beamDict["total_beams"]):
                if (
                    self.ids.coherent_wave[beamIndex]
                    .beam_tracing[beamTracingTimeIndex]
                    .beam[rayIndex]
                    .power_initial
                    > 0
                ):
                    # todo: this will loop and overwrite value, is it intended?
                    beamDict["active"] = True
            activeBeams[beamIndex] = beamDict

        return activeBeams

    def getBeamTracing(self, beamTracingTimeIndex: int = 0):
        """
        This function returns a dictionary containing information about the beam tracing of a coherent wave.

        Args:
            beamTracingTimeIndex (int): The index of the time step for which to retrieve the beam tracing data. Defaults to 0

        Returns:
            a dictionary named "beam_tracing" which contains various arrays and values related to the beam tracing data. Following are the values returned by the function

            - nbeam
            - nbeam_active
            - nray
            - is_active
            - len_ray
            - x_ray
            - y_ray
            - z_ray
            - r_ray
            - phi_ray
            - central_ray_power
            - central_ray_powerpar
            - central_ray_powerperp
            - central_ray_length
        """
        # Count number of active beams and their number of rays
        activeBeamsDict = self.getActiveBeams(beamTracingTimeIndex)
        totalWaves = len(activeBeamsDict.keys())
        activeBeamsArray = [data["active"] for _, data in activeBeamsDict.items()]
        totalBeamsArray = [data["total_beams"] for _, data in activeBeamsDict.items()]

        # We assume the same number of rays for each beam, to simplify (and this is usually the case)
        maxTotalBeams = max(totalBeamsArray)

        arrayLength = max(
            max(
                [
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[rayIndex]
                        .position.r
                    )
                    for rayIndex in range(maxTotalBeams)
                ]
                for beamIndex in range(totalWaves)
            )
        )
        len_ray = np.array(
            [[0.0 for _ in range(maxTotalBeams)] for _ in range(totalWaves)]
        ).astype(int)
        x_ray = np.array(
            [
                [[0.0 for _ in range(arrayLength)] for _ in range(maxTotalBeams)]
                for _ in range(totalWaves)
            ]
        )
        y_ray, z_ray, r_ray, phi_ray = (
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
            np.ndarray.copy(x_ray),
        )

        central_ray_power = np.array(
            [[0.0 for _ in range(arrayLength)] for _ in range(totalWaves)]
        )
        central_ray_powerpar, central_ray_powerperp, central_ray_length = (
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
            np.ndarray.copy(central_ray_power),
        )
        wr = []
        for beamIndex in range(totalWaves):
            if activeBeamsArray[beamIndex] == 1:
                for iray in range(maxTotalBeams):
                    if (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[iray]
                        .power_initial
                        != 0
                    ):
                        wr = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.r
                        )
                        wphi = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.phi
                        )
                        wz = (
                            self.ids.coherent_wave[beamIndex]
                            .beam_tracing[beamTracingTimeIndex]
                            .beam[iray]
                            .position.z
                        )
                        len_ray[beamIndex, iray] = len(wr)
                        r_ray[beamIndex, iray, : len(wr)] = np.array(wr)
                        phi_ray[beamIndex, iray, : len(wphi)] = np.array(wphi)
                        z_ray[beamIndex, iray, : len(wz)] = np.array(wz)
                        x_ray[beamIndex, iray, :] = r_ray[beamIndex, iray, :] * np.cos(
                            phi_ray[beamIndex, iray, :]
                        )
                        y_ray[beamIndex, iray, :] = r_ray[beamIndex, iray, :] * np.sin(
                            phi_ray[beamIndex, iray, :]
                        )
                    npath = len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                    > 0
                ):
                    central_ray_power[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .electrons.power
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                    > 0
                ):
                    central_ray_powerpar[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.parallel
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                    > 0
                ):
                    central_ray_powerperp[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .power_flow_norm.perpendicular
                    )
                if (
                    len(
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .length
                    )
                    > 0
                ):
                    central_ray_length[beamIndex, 0:npath] = (
                        self.ids.coherent_wave[beamIndex]
                        .beam_tracing[beamTracingTimeIndex]
                        .beam[0]
                        .length
                    )

        beam_tracing = {"nbeam": totalWaves}
        beam_tracing["nbeam_active"] = len(activeBeamsArray)
        beam_tracing["nray"] = maxTotalBeams
        beam_tracing["is_active"] = activeBeamsArray
        beam_tracing["len_ray"] = len_ray
        beam_tracing["x_ray"] = x_ray
        beam_tracing["y_ray"] = y_ray
        beam_tracing["z_ray"] = z_ray
        beam_tracing["r_ray"] = r_ray
        beam_tracing["phi_ray"] = phi_ray[:, :, : len(wr)]
        beam_tracing["central_ray_power"] = central_ray_power
        beam_tracing["central_ray_powerpar"] = central_ray_powerpar
        beam_tracing["central_ray_powerperp"] = central_ray_powerperp
        beam_tracing["central_ray_length"] = central_ray_length

        return beam_tracing
