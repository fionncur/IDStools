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

    def getActivePfCoils(self) -> dict:
        """
        This function returns a dictionary of active PF coils and their corresponding elements dimensions and center coordinates.

        Returns:
            a dictionary containing information about the active PF (poloidal field) coils. The keys of the dictionary are the identifiers of the coils, and the values are dictionaries containing information about the individual elements of each coil. The information about each element includes its horizontal width, vertical height, and center coordinates.

        Examples:
            .. code-block:: python

                import pprint
                import imas
                from idstools.compute.pf_active import PfActiveCompute
                from idstools.view.common import Canvas
                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=135005;run=4;database=ITER;version=3", "r")
                connection.open()
                idsObj = connection.get('pf_active')

                computeObj = PfActiveCompute(idsObj)
                result=computeObj.getActivePfCoils()
                pprint.pprint(result)
        """

        coils = {}
        for coilIndex, coil in enumerate(self.ids.coil):
            coilInfo = {}

            coilInfo["identifier"] = coil.identifier
            coilInfo["name"] = coil.name
            coilInfo["resistance"] = coil.resistance

            # Get elements
            dictElements = {}
            for elementIndex, element in enumerate(coil.element):
                horizontalWidth = element.geometry.rectangle.width
                verticalHeight = element.geometry.rectangle.height
                if horizontalWidth > 0.0 and verticalHeight > 0.0:
                    cec = (
                        element.geometry.rectangle.r - horizontalWidth / 2.0,
                        element.geometry.rectangle.z - verticalHeight / 2.0,
                    )
                    dictElements[elementIndex] = {
                        "name": element.name,
                        "identifier": element.identifier,
                        "area": element.area,
                        "horizontalWidth": horizontalWidth,
                        "horizontalHeight": verticalHeight,
                        "cec": cec,
                        "r": element.geometry.rectangle.r,
                        "z": element.geometry.rectangle.z,
                    }

            coilInfo["elements"] = dictElements
            if not dictElements:
                logger.warning(f"Coil index {coilIndex} : pf_active.coil.element.geometry.rectangle is empty")
            coils[coilIndex] = coilInfo
        if not coils:
            logger.warning("pf_active.coil is empty")
        return coils
