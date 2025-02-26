"""
This module provides compute functions and classes for pf_passive ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger("module")


class PfPassiveCompute:
    """This class provides compute functions for pf_passive ids"""

    def __init__(self, ids: object):
        """Initialization PfPassiveCompute object.

        Args:
            ids : pf_passive ids object
        """
        self.ids = ids

    def get_pf_passive_loops(self, select=":") -> dict:
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
        loop_arrays = list(self.ids.loop)
        if select is not None:
            loop_arrays = get_slice_from_array(loop_arrays, select)
        loops = {}
        for loop_index, loop in enumerate(loop_arrays):
            loop_info = {}
            if hasattr(loop, "identifier"):
                loop_info["identifier"] = loop.identifier
            else:
                loop_info["identifier"] = ""
            loop_info["name"] = loop.name
            loop_info["resistance"] = loop.resistance
            loop_info["resistivity"] = loop.resistivity

            dict_elements = {}

            for element_index, element in enumerate(loop.element):

                if hasattr(element, "identifier"):
                    element_identifier = element.identifier
                else:
                    element_identifier = ""
                dict_element = {}
                dict_element["name"] = element.name
                dict_element["identifier"] = element_identifier
                dict_element["geometry_type"] = element.geometry.geometry_type
                if element.geometry.geometry_type == 1:  # outline
                    dict_element["r"] = element.geometry.outline.r
                    dict_element["z"] = element.geometry.outline.z
                elif element.geometry.geometry_type == 2:  # rectangle
                    dict_element["r"] = element.geometry.rectangle.r
                    dict_element["z"] = element.geometry.rectangle.z
                    dict_element["width"] = element.geometry.rectangle.width
                    dict_element["height"] = element.geometry.rectangle.height
                elif element.geometry.geometry_type == 3:  # oblique
                    dict_element["r"] = element.geometry.oblique.r
                    dict_element["z"] = element.geometry.oblique.z
                    dict_element["length_alpha"] = element.geometry.oblique.length_alpha
                    dict_element["length_beta"] = element.geometry.oblique.length_beta
                    dict_element["alpha"] = element.geometry.oblique.alpha
                    dict_element["beta"] = element.geometry.oblique.beta
                elif element.geometry.geometry_type == 4:  # arcs_of_circle
                    dict_element["r"] = element.geometry.arcs_of_circle.r
                    dict_element["z"] = element.geometry.arcs_of_circle.z
                    dict_element["curvature_radii"] = element.geometry.arcs_of_circle.curvature_radii
                elif element.geometry.geometry_type == 5:  # annulus
                    dict_element["r"] = element.geometry.annulus.r
                    dict_element["z"] = element.geometry.annulus.z
                    dict_element["radius_inner"] = element.geometry.annulus.radius_inner
                    dict_element["radius_outer"] = element.geometry.annulus.radius_outer
                elif element.geometry.geometry_type == 6:  # thick_line
                    dict_element["r1"] = element.geometry.thick_line.first_point.r
                    dict_element["z1"] = element.geometry.thick_line.first_point.z
                    dict_element["r2"] = element.geometry.thick_line.second_point.r
                    dict_element["z2"] = element.geometry.thick_line.second_point.z
                    dict_element["thickness"] = element.geometry.thick_line.thickness
                else:
                    dict_element["r"] = element.geometry.outline.r
                    dict_element["z"] = element.geometry.outline.z
                dict_elements[element_index] = dict_element

            loop_info["elements"] = dict_elements
            if not dict_elements:
                logger.warning(f"loop index {loop_index} : pf_passive.loop.element.geometry.thick_line is empty")
            loops[loop_index] = loop_info
        if not loops:
            logger.warning("pf_passive.loop is empty")
            return None
        return loops
