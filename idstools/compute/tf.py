"""
This module provides compute functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger("module")


class TFCompute:
    """This class provides compute functions for tf ids"""

    def __init__(self, ids: object):
        """Initialization PfPassiveCompute object.

        Args:
            ids : tf ids object
        """
        self.ids = ids

    def get_tf_coils(self, select_coil=":", select_conductor=":") -> dict:
        """
        Retrieve information about the Toroidal Field (TF) coils and their conductors.

        Args:
            select_coil (str, optional): A string representing the selection of coils.
                         Defaults to ":" which selects all coils.
            select_conductor (str, optional): A string representing the selection of conductors.
                              Defaults to ":" which selects all conductors.

        Returns:
            dict: A dictionary containing information about the selected TF coils and their conductors.
              The dictionary structure is as follows:
              {
                  coil_index: {
                  "identifier": str,
                  "name": str,
                  "resistance": float,
                  "turns": int,
                  "conductors": {
                      conductor_index: {
                      "elements": list,
                      "cross_section": float
                      }
                  }
                  }
              }
              If no coils are found, a warning is logged and None is returned.
        """
        coil_arrays = list(self.ids.coil)
        if select_coil is not None:
            coil_arrays = get_slice_from_array(coil_arrays, select_coil)
        coils = {}
        for coil_index, coil in enumerate(coil_arrays):
            coil_info = {}
            if hasattr(coil, "identifier"):
                coil_info["identifier"] = coil.identifier
            else:
                coil_info["identifier"] = ""
            coil_info["name"] = coil.name
            coil_info["resistance"] = coil.resistance
            coil_info["turns"] = coil.turns
            conductor_arrays = list(coil.conductor)
            if select_conductor is not None:
                conductor_arrays = get_slice_from_array(conductor_arrays, select_conductor)
            conductors = {}
            for conductor_index, conductor in enumerate(conductor_arrays):
                conductor_info = {}
                conductor_info["elements"] = conductor.elements
                conductor_info["cross_section"] = conductor.cross_section
                conductors[conductor_index] = conductor_info

            coil_info["conductors"] = conductors
            coils[coil_index] = coil_info
        if not coils:
            logger.warning("tf.coil is empty")
            return None
        return coils
