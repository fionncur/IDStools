"""
This module provides view functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
from matplotlib.patches import Patch, Polygon

from idstools.compute.tf import TFCompute

logger = logging.getLogger("module")


class TFView:
    """This class provides view functions for tf ids"""

    def __init__(self, ids: object):
        """Initialization TFView object.

        Args:
            ids : tf ids object
        """
        self.ids = ids
        self.compute_obj = TFCompute(ids)

    def view_tf_coils(self, ax: plt.axes, select_coil=":", select_conductor="", color="#b07154"):
        """
        Plots the Toroidal Field (TF) coils on the given matplotlib axis.

        Parameters:
        ax (plt.axes): The matplotlib axis to plot on.
        select_coil (str, optional): The coil selection criteria. Defaults to ":".
        select_conductor (str, optional): The conductor selection criteria. Defaults to "".
        color (str, optional): The color to use for plotting the coils. Defaults to "#800000".
        show_labels (bool, optional): Whether to show labels for the coils. Defaults to False.

        Returns:
        Patch: A matplotlib Patch object for the TF legend.

        Notes:
        - The function retrieves TF coil data using the compute_obj's get_tf_coils method.
        - If no TF coil data is found, a warning is logged and the function returns without plotting.
        - The function plots the start and end points of the coil conductors and connects them with line segments.
        - If show_labels is True, the coil identifiers or names are displayed as text labels.
        - The aspect ratio of the plot is set to be equal and the title is updated to include "tf".
        """
        coils_dict = self.compute_obj.get_tf_coils(select_coil=select_coil, select_conductor=select_conductor)

        if coils_dict is None:
            logger.warning("Can not plot, no tf coils data found.")
            return
        for _, coil_info in coils_dict.items():
            conductors = coil_info["conductors"]
            if hasattr(coil_info, "identifier"):
                name = coil_info["identifier"]
            else:
                name = coil_info["name"]

            cx = 0
            cy = 0
            for _, conductor_info in conductors.items():
                elements = conductor_info["elements"]
                # cross_sections = conductor_info["cross_section"]
                ax.scatter(elements["start_points"]["r"], elements["start_points"]["z"], color=color, s=10)
                ax.scatter(elements["end_points"]["r"], elements["end_points"]["z"], color=color, s=10)
                for ielement in range(len(elements.types)):
                    if elements["types"][ielement] == 1:  # line

                        r1 = elements["start_points"]["r"][ielement]
                        z1 = elements["start_points"]["z"][ielement]
                        r2 = elements["end_points"]["r"][ielement]
                        z2 = elements["end_points"]["z"][ielement]
                        if ielement == 0:
                            cx = r1
                            cy = z1
                        segment = Polygon(
                            [[r1, z1], [r2, z2]], closed=False, edgecolor=color, facecolor="none", linewidth=1
                        )
                        ax.add_patch(segment)

            name = ""
            if coil_info["identifier"]:
                name = coil_info["identifier"]
            elif coil_info["name"]:
                name = f"{coil_info['name']}"

            ax.text(cx, cy, name, fontsize="small", color="#333333", visible=False)
        tf_legend = Patch(color=color, label="tf")

        ax.set_aspect("equal", adjustable="box")
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, tf")
        else:
            ax.set_title("tf")
        return tf_legend
