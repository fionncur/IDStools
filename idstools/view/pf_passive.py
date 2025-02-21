"""
This module provides view functions and classes for pf_passive ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from idstools.compute.pf_passive import PfPassiveCompute

logger = logging.getLogger("module")


class PFPassiveView:
    """This class provides view functions for pf_passive ids"""

    def __init__(self, ids: object):
        """Initialization PFPassiveView object.

        Args:
            ids : pf_passive ids object
        """
        self.ids = ids
        self.compute_obj = PfPassiveCompute(ids)

    def view_pf_passive_loops(self, ax: plt.axes, show_labels=False):
        """
        Visualizes passive PF (Poloidal Field) loops on the given matplotlib axis.

        Parameters:
        ax (plt.axes): The matplotlib axes on which to draw the PF loops.
        show_labels (bool, optional): If True, labels the loops with their identifiers or names. Defaults to False.

        This method retrieves active PF loops from the compute object and draws them as rectangles on the provided
        matplotlib axis. Each rectangle represents a loop element, and the rectangles are colored with a blue edge
        and cyan face with 50% transparency. If `show_labels` is True, the method labels each rectangle with the
        loop's identifier or name at the center of the rectangle. The aspect ratio of the plot is set to be equal,
        and the plot title is appended with ", pf_passive".
        """
        loops_dict = self.compute_obj.get_pf_passive_loops()
        if loops_dict is None:
            logger.warning("Can not plot, no pf passive loops data found.")
            return
        for _, loop_info in loops_dict.items():
            loop_elements = loop_info["elements"]

            for _, element_info in loop_elements.items():
                if loop_info["geometry_type"] == 6:
                    r1, r2, z1, z2 = (
                        element_info["r1"],
                        element_info["r2"],
                        element_info["z1"],
                        element_info["z2"],
                    )
                    width = abs(r2 - r1)
                    height = abs(z2 - z1)
                    rectangle = Rectangle(
                        (min(r1, r2), min(z1, z2)), width, height, edgecolor="blue", facecolor="cyan", alpha=0.5
                    )
                if loop_info["geometry_type"] == 1:
                    width = 0.2
                    height = 0.2
                    r, z = (
                        element_info["r"],
                        element_info["z"],
                    )
                    rectangle = Rectangle((r, z), width, height, edgecolor="blue", facecolor="cyan", alpha=0.5)
                ax.add_patch(rectangle)
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width() / 2.0
                cy = ry + rectangle.get_height() / 2.0

                if show_labels:
                    name = ""
                    if loop_info["identifier"]:
                        name = loop_info["identifier"]
                    elif loop_info["name"]:
                        name = f"{loop_info['name']}"

                    ax.text(
                        cx,
                        cy,
                        name,
                        fontsize="x-small",
                    )

        ax.set_aspect("equal", adjustable="box")
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, pf_passive")
        else:
            ax.set_title("pf_passive")
