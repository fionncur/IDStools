"""
This module provides compute functions and classes for pf_passive ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

logger = logging.getLogger("module")


class PfPassiveCompute:
    """This class provides compute functions for pf_passive ids"""

    def __init__(self, ids: object):
        """Initialization PfPassiveCompute object.

        Args:
            ids : pf_passive ids object
        """
        self.ids = ids

    def get_pf_passive_loops(self) -> dict:
        """
        Retrieves passive loops information from the IDS (Integrated Data Structure).

        This method processes the loops and their elements, extracting relevant information
        such as identifiers, names, resistances, resistivities, and geometrical coordinates.
        It returns a dictionary where each key is the loop index and the value is another
        dictionary containing loop details and its elements.

        Returns:
            dict: A dictionary containing loop information and their elements.
                  Returns None if no valid loops are found or if the geometry type is not implemented.

        Raises:
            None

        Logs:
            Warnings are logged if:
            - The geometry type is not implemented.
            - Any loop has no elements.
            - The entire loop structure is empty.
        """

        loops = {}
        geometry_type = 0
        if len(self.ids.loop) > 0 and len(self.ids.loop[0].element) > 0:
            geometry_type = self.ids.loop[0].element[0].geometry.geometry_type
            if not self.ids.loop[0].element[0].geometry.geometry_type.has_value:
                geometry_type = 1
            if geometry_type != 6 and geometry_type != 1:
                logger.warning(
                    "pf_passive.loop.element.geometry.geometry_type"
                    f"{self.ids.loop[0].element[0].geometry.geometry_type} is not implemented"
                )
                return None
        for loop_index, loop in enumerate(self.ids.loop):
            loop_info = {}
            if hasattr(loop, "identifier"):
                loop_info["identifier"] = loop.identifier
            else:
                loop_info["identifier"] = ""
            loop_info["name"] = loop.name
            loop_info["resistance"] = loop.resistance
            loop_info["resistivity"] = loop.resistivity

            dict_elements = {}
            loop_info["geometry_type"] = geometry_type

            for element_index, element in enumerate(loop.element):

                if hasattr(element, "identifier"):
                    element_identifier = element.identifier
                else:
                    element_identifier = ""

                dict_elements[element_index] = {
                    "name": element.name,
                    "identifier": element_identifier,
                    "r": element.geometry.outline.r,
                    "z": element.geometry.outline.z,
                    "r1": element.geometry.thick_line.first_point.r,
                    "z1": element.geometry.thick_line.first_point.z,
                    "r2": element.geometry.thick_line.second_point.r,
                    "z2": element.geometry.thick_line.second_point.z,
                }

            loop_info["elements"] = dict_elements
            if not dict_elements:
                logger.warning(f"loop index {loop_index} : pf_passive.loop.element.geometry.thick_line is empty")
            loops[loop_index] = loop_info
        if not loops:
            logger.warning("pf_passive.loop is empty")
            return None
        return loops
