"""
This module provides compute functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

logger = logging.getLogger("module")


class PfActiveCompute:
    """This class provides compute functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization PfActiveCompute object.

        Args:
            ids : pf_active ids object
        """
        self.ids = ids

    def get_active_pf_coils(self) -> dict:
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
                import imaspy as imas
                from idstools.compute.pf_active import PfActiveCompute
                from idstools.view.common import PlotCanvas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=135005;run=4;database=ITER;version=3", "r")
                idsObj = connection.get('pf_active')

                computeObj = PfActiveCompute(idsObj)
                result=computeObj.get_active_pf_coils()
                pprint.pprint(result)
        """

        coils = {}
        # rectangle is geometry_type 2
        if (
            len(self.ids.coil) > 0
            and len(self.ids.coil[0].element) > 0
            and self.ids.coil[0].element[0].geometry.geometry_type != 2
        ):
            logger.warning(
                "pf_active.coil.element.geometry.geometry_type"
                f"{self.ids.coil[0].element[0].geometry.geometry_type} is not implemented"
            )
            return None
        for coil_index, coil in enumerate(self.ids.coil):
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
                horizontal_width = element.geometry.rectangle.width
                vertical_height = element.geometry.rectangle.height
                if horizontal_width > 0.0 and vertical_height > 0.0:
                    cec = (
                        element.geometry.rectangle.r - horizontal_width / 2.0,
                        element.geometry.rectangle.z - vertical_height / 2.0,
                    )
                    if hasattr(element, "identifier"):
                        element_identifier = element.identifier
                    else:
                        element_identifier = ""

                    dict_elements[element_index] = {
                        "name": element.name,
                        "identifier": element_identifier,
                        "area": element.area,
                        "horizontal_width": horizontal_width,
                        "horizontal_height": vertical_height,
                        "cec": cec,
                        "r": element.geometry.rectangle.r,
                        "z": element.geometry.rectangle.z,
                    }

            coil_info["elements"] = dict_elements
            if not dict_elements:
                logger.warning(f"Coil index {coil_index} : pf_active.coil.element.geometry.rectangle is empty")
            coils[coil_index] = coil_info
        if not coils:
            logger.warning("pf_active.coil is empty")
        return coils
