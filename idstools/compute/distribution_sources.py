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

    def get_rho_tor_norm(self, time_slice: int, source_index=0) -> Union[None, np.ndarray]:
        """
        The function `get_rho_tor_norm` returns the normalized toroidal rho values from a given time slice
        of a source.

        Args:
            time_slice (int): The parameter "time_slice" is an integer that represents the time slice for
                which you want to retrieve the value of "rho_tor_norm".

        Returns:
            the variable `rho_tor_norm`.
        """
        rho_tor_norm = None
        try:
            rho_tor_norm = self.ids.source[source_index].profiles_1d[time_slice].grid.rho_tor_norm
            if len(rho_tor_norm) == 0 and len(self.ids.source[source_index].profiles_1d[time_slice].grid.rho_tor) > 0:
                nrho = len(self.ids.source[source_index].profiles_1d[time_slice].grid.rho_tor)
                rho_tor_norm = (
                    self.ids.source[source_index].profiles_1d[time_slice].grid.rho_tor
                    / self.ids.source[source_index].profiles_1d[time_slice].grid.rho_tor[nrho - 1]
                )
        except Exception as e:
            logger.debug(f"{e}")
            logger.critical(
                f"distribution_sources.source[{source_index}].profiles_1d[{time_slice}].grid.rho_tor_norm)"
                "could not be read"
            )
        return rho_tor_norm

    def get_volume(self, time_slice: int, source_index=0) -> Union[None, np.ndarray]:
        """
        The function `get_volume` retrieves the volume from a specific time slice of a source's profiles.

        Args:
            time_slice (int): The parameter "time_slice" is an optional integer that specifies the index of the time
                slice for which you want to retrieve the volume.

        Returns:
            the volume of a grid at a given time slice. The volume is obtained from the
            `distribution_sources.source[time_slice].profiles_1d[0].grid.volume` attribute.If the volume cannot be read
            , the function returns `None`.
        """
        volume = None
        try:
            volume = self.ids.source[source_index].profiles_1d[time_slice].grid.volume
        except Exception as e:
            logger.debug(f"{e}")
            logger.critical(
                f"distribution_sources.source[{source_index}].profiles_1d[{time_slice}].grid.volume"
                "could not be read {e}"
            )
        return volume

    def get_source_info(self, time_slice, process_index=0):
        """
        The function `get_source_info` retrieves information about sources, including labels, particle data, and power,
        and returns it in a dictionary format.

        Returns:
            a dictionary called `sources_dict`.
        """
        nrho = len(self.get_rho_tor_norm(time_slice))
        sources_dict = {}
        counter = 0
        for isource, source in enumerate(self.ids.source):
            mlabel1 = unicodedata.normalize("NFKD", source.process[process_index].type.description.value).encode(
                "ascii", "ignore"
            )
            mlabel2 = unicodedata.normalize(
                "NFKD", source.process[process_index].reactant_energy.description.value
            ).encode("ascii", "ignore")
            particles = source.profiles_1d[time_slice].particles
            if len(source.profiles_1d[time_slice].particles) < 1:
                logger.warning(
                    f"distribution_sources.source[{isource}].profiles_1d[{time_slice}].particles could not be read"
                )
                particles = np.asarray([np.nan] * nrho)

            source_info = {
                "label": (mlabel1 + b"; " + mlabel2).decode(),
                "particles": particles,
                "powerInKW": source.global_quantities[time_slice].power * 1.0e-3,
            }
            sources_dict[counter] = source_info
            counter = counter + 1
        return sources_dict
