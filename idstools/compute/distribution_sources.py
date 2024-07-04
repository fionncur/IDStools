"""
This module provides compute functions and classes for distribution_sources ids data

"""

import logging
import unicodedata
from typing import Union

import numpy as np

logger = logging.getLogger("module")


class DistributionSourcesCompute:
    def __init__(self, ids):
        self.ids = ids

    def getRhoTorNorm(self, timeSlice: int = 0) -> Union[None, np.ndarray]:
        """
        The function `getRhoTorNorm` returns the normalized toroidal rho values from a given time slice
        of a source.

        Args:
            timeSlice (int): The parameter "timeSlice" is an integer that represents the time slice for which you want to retrieve the value of "rho_tor_norm".

        Returns:
            the variable `rho_tor_norm`.
        """
        rho_tor_norm = None
        try:
            rho_tor_norm = self.ids.source[0].profiles_1d[timeSlice].grid.rho_tor_norm
            if len(rho_tor_norm) == 0 and len(self.ids.source[0].profiles_1d[timeSlice].grid.rho_tor) > 0:
                nrho = len(self.ids.source[0].profiles_1d[timeSlice].grid.rho_tor)
                rho_tor_norm = (
                    self.ids.source[0].profiles_1d[timeSlice].grid.rho_tor
                    / self.ids.source[0].profiles_1d[timeSlice].grid.rho_tor[nrho - 1]
                )
        except Exception as e:
            logger.critical("distribution_sources.source[0].profiles_1d[0].grid.rho_tor(_norm) could not be read")
        return rho_tor_norm

    def getVolume(self, timeSlice: int = 0) -> Union[None, np.ndarray]:
        """
        The function `getVolume` retrieves the volume from a specific time slice of a source's profiles.

        Args:
            timeSlice (int): The parameter "timeSlice" is an optional integer that specifies the index of the time slice for which you want to retrieve the volume.

        Returns:
            the volume of a grid at a given time slice. The volume is obtained from the `distribution_sources.source[timeSlice].profiles_1d[0].grid.volume` attribute. If the volume cannot be read, the function returns `None`.
        """
        volume = None
        try:
            volume = self.ids.source[0].profiles_1d[timeSlice].grid.volume
        except Exception as e:
            logger.critical(f"distribution_sources.source[0].profiles_1d[{timeSlice}].grid.volume could not be read")
        return volume

    def getSourceInfo(self):
        """
        The function `getSourceInfo` retrieves information about sources, including labels, particle data, and power, and returns it in a dictionary format.

        Returns:
            a dictionary called `sourcesDict`.
        """
        nrho = len(self.getRhoTorNorm())
        sourcesDict = {}
        counter = 0
        for source in self.ids.source:
            mlabel1 = unicodedata.normalize("NFKD", source.process[0].type.description).encode("ascii", "ignore")
            mlabel2 = unicodedata.normalize("NFKD", source.process[0].reactant_energy.description).encode(
                "ascii", "ignore"
            )
            particles = source.profiles_1d[0].particles
            if len(source.profiles_1d[0].particles) < 1:
                logger.warning("distribution_sources.source[isource].profiles_1d[0].particles could not be read")
                particles = np.asarray([np.nan] * nrho)

            sourceInfo = {
                "label": (mlabel1 + b"; " + mlabel2).decode(),
                "particles": particles,
                "powerInKW": source.global_quantities[0].power * 1.0e-3,
            }
            sourcesDict[counter] = sourceInfo
            counter = counter + 1
        return sourcesDict
