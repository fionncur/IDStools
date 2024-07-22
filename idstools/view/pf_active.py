"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/i_m_design/Data%20Model/sphinx/latest.html>`_.

"""

import logging
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt

from idstools.compute.pf_active import PfActiveCompute

logger = logging.getLogger("module")


class p_f_active_view:
    """This class provides view functions for pf_active ids"""

    def __init__(self, ids_obj: object):
        """Initialization PFActiveView object.

        Args:
            idsObj : pf_active ids object
        """
        self.ids_obj = ids_obj
        self.compute_obj = pf_active_compute(ids_obj)

    def view_active_pf_coils(self, ax: plt.axes, show_labels=False):
        """
        This function plots and annotates the active PF coils on a existing plot.

        Args:
            ax (plt.axes): `ax` is a parameter of type `plt.axes`, It is used to add patches (such as rectangles)
            and annotations to the plot.

        Example:
            .. code-block:: python

                import imas
                from idstools.view.pf_active import PFActiveView
                from idstools.view.common import Canvas

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=135005;run=4;database=ITER;version=3", "r")
                connection.open()
                idsObj = connection.get('pf_active')
                connection.close()
                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

                viewObj = PfActiveView(idsObj)
                viewObj.viewActivePfCoils(ax) # plot contour on the canvas axes

                ax.plot()
                canvas.show()

            .. thumbnail:: /_static/images/PFActiveView_viewActivePfCoils.png
                :alt: image not found
                :align: center
        """
        if coils_dict := self.compute_obj.get_active_pf_coils():
            for _, coil_info in coils_dict.items():
                coil_elements = coil_info["elements"]
                for _, element_info in coil_elements.items():
                    cew, ceh, cec = (
                        element_info["horizontalWidth"],
                        element_info["horizontalHeight"],
                        element_info["cec"],
                    )
                    rectangle = rectangle(cec, cew, ceh, edgecolor="#fd7e14", facecolor="#fd7e14")

                    ax.add_patch(rectangle)
                    rx, ry = rectangle.get_xy()
                    cx = rx + rectangle.get_width() / 2.0
                    cy = ry + rectangle.get_height() / 2.0

                    if show_labels:
                        name = ""
                        if coil_info["identifier"]:
                            name = coil_info["identifier"]
                        elif coil_info["name"]:
                            name = f"{coil_info['name']}"

                        ax.text(
                            cx,
                            cy,
                            name,
                            fontsize="x-small",
                            rotation=90,
                        )
            ax.set_aspect("equal", adjustable="box")
