"""
This module provides compute functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

from idstools.utils.utility_functions import get_slice_from_array

logger = logging.getLogger("module")


class PfActiveCompute:
    """This class provides compute functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization PfActiveCompute object.

        Args:
            ids : pf_active ids object
        """
        self.ids = ids

    def get_active_pf_coils(self, select=":") -> dict:
        """
        This function returns a dictionary of active PF coils and their corresponding elements dimensions and
        center coordinates.

        Returns:
            a dictionary containing information about the active PF (poloidal field) coils. The keys of the dictionary
            are the identifiers of the coils, and the values are dictionaries containing information about the
            individual elements of each coil. The information about each element includes its horizontal width,
            vertical height, and center coordinates.

        Examples:
            .. code-block:: python

                import pprint
                import imas
                from idstools.compute.pf_active import PfActiveCompute
                from idstools.view.common import PlotCanvas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=135005;run=4;database=ITER;version=3", "r")
                idsObj = connection.get('pf_active')

                computeObj = PfActiveCompute(idsObj)
                result=computeObj.get_active_pf_coils()
                pprint.pprint(result)
        """
        coil_arrays = list(self.ids.coil)
        if select is not None:
            coil_arrays = get_slice_from_array(coil_arrays, select)
        coils = {}
        for coil_index, coil in enumerate(coil_arrays):

            coil_info = {}
            if hasattr(coil, "identifier"):
                coil_info["identifier"] = coil.identifier
            else:
                coil_info["identifier"] = ""
            coil_info["name"] = coil.name
            coil_info["resistance"] = coil.resistance

            # Get elements
            dict_elements = {}

            for element_index, element in enumerate(coil.element):
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
                dict_elements[element_index] = dict_element
            coil_info["elements"] = dict_elements
            if not dict_elements:
                logger.warning(f"Coil index {coil_index} : pf_active.coil.element.geometry.rectangle is empty")
            coils[coil_index] = coil_info
        if not coils:
            logger.warning("pf_active.coil is empty")
        return coils
