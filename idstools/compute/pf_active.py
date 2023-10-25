""" 
This module provides compute functions and classes for pf_active ids data

`more about pf_active ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/pf_active.html>`_

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

                connection = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',135005,4,'public')
                connection.open()
                idsObj = connection.get('pf_active')

                computeObj = PfActiveCompute(idsObj)
                result=computeObj.getActivePfCoils()
                pprint.pprint(result)

                {'CS1L': {'element0': (0.74, 2.093, (1.3170000000000002, -2.1185))},
                'CS1U': {'element0': (0.74,2.093,(1.3170000000000002, 0.045500000000000096))},
                'CS2L': {'element0': (0.74, 2.093, (1.3170000000000002, -4.3045))},
                'CS2U': {'element0': (0.74, 2.093, (1.3170000000000002, 2.2315))},
                'CS3L': {'element0': (0.74, 2.093, (1.3170000000000002, -6.4905))},
                'CS3U': {'element0': (0.74, 2.093, (1.3170000000000002, 4.4175))},
                'PF1': {'element0': (0.959, 0.9841, (3.4636, 7.08205))},
                'PF2': {'element0': (0.5801, 0.7146, (7.99505, 6.182499999999999))},
                'PF3': {'element0': (0.6963, 0.9538, (11.643749999999999, 2.7983))},
                'PF4': {'element0': (0.6382, 0.9538, (11.643899999999999, -2.7105))},
                'PF5': {'element0': (0.8125, 0.9538, (7.9845500000000005, -7.2038))},
                'PF6': {'element0': (1.559, 1.1075, (3.5544999999999995, -8.02025))}}
        """

        coils = {}
        for coil in self.ids.coil:
            dictElements = {}
            for index, element in enumerate(coil.element):
                horizontalWidth = element.geometry.rectangle.width
                verticalHeight = element.geometry.rectangle.height
                if horizontalWidth > 0.0 and verticalHeight > 0.0:
                    cec = (
                        element.geometry.rectangle.r - horizontalWidth / 2.0,
                        element.geometry.rectangle.z - verticalHeight / 2.0,
                    )
                    dictElements[f"element{str(index)}"] = (
                        horizontalWidth,
                        verticalHeight,
                        cec,
                    )
            if dictElements:
                coils[coil.identifier] = dictElements
            else:
                logger.warning(
                    f"{coil.identifier} : pf_active.coil.element.geometry.rectangle is empty"
                )

        if not coils:
            logger.warning("pf_active.coil is empty")
        return coils
