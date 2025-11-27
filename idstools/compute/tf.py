"""
This module provides compute functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging
import math

import numpy as np
from idstools.compute.common import get_conductor_outline
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
                # Add outline only for line segment elements with valid cross-section
                if np.all(conductor.elements.types == 1) and len(conductor.cross_section) == 1:
                    n = len(conductor.elements.start_points.r)
                    nskip = max(1, math.ceil(n / 180))
                    conductor_info["outline"] = get_conductor_outline(conductor, skip=nskip)
                conductors[conductor_index] = conductor_info

            coil_info["conductors"] = conductors
            coils[coil_index] = coil_info
        if not coils:
            logger.warning("tf.coil is empty")
            return None
        return coils
