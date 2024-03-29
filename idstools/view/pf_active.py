""" 
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""
import logging
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

from idstools.compute.pf_active import PfActiveCompute

logger = logging.getLogger("module")


class PFActiveView:
    """This class provides view functions for pf_active ids"""

    def __init__(self, idsObj: object):
        """Initialization PFActiveView object.

        Args:
            idsObj : pf_active ids object
        """
        self.idsObj = idsObj
        self.computeObj = PfActiveCompute(idsObj)

    def viewActivePfCoils(self, ax: plt.axes):
        """
        This function plots and annotates the active PF coils on a existing plot.

        Args:
            ax (plt.axes): `ax` is a parameter of type `plt.axes`, It is used to add patches (such as rectangles) and annotations to the plot.

        Example:
            .. code-block:: python

                import imas
                from idstools.view.pf_active import PFActiveView
                from idstools.view.common import Canvas

                input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',135005,4,'public')
                input.open()
                idsObj = input.get('pf_active')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

                viewObj = PfActiveView(idsObj)
                viewObj.viewActivePfCoils(ax) # plot contour on the canvas axes

                ax.plot()
                canvas.show()

            .. image:: ../_static/images/PFActiveView_viewActivePfCoils.png
                :alt: image not found
                :align: center
        """
        if dictCoils := self.computeObj.getActivePfCoils():
            for coilIdentifier, coilElements in dictCoils.items():
                for _, dimension in coilElements.items():
                    cew, ceh, cec = dimension
                    rectangle = Rectangle(cec, cew, ceh)

                    ax.add_patch(rectangle)
                    rx, ry = rectangle.get_xy()
                    cx = rx + rectangle.get_width() / 2.0
                    cy = ry + rectangle.get_height() / 2.0
                    ax.annotate(
                        coilIdentifier,
                        (cx, cy),
                        color="black",
                        weight="bold",
                        ha="center",
                        va="center",
                    )
            ax.set_aspect("equal", adjustable="box")

        else:
            logger.error("No PF Coils found in the IDS data")
