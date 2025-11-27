"""
This module provides view functions and classes for tf ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
import matplotlib.text as mtext
import numpy as np
from matplotlib.patches import Patch, Polygon

from idstools.compute.tf import TFCompute

logger = logging.getLogger(__name__)


class TFView:
    """This class provides view functions for tf ids"""

    def __init__(self, ids: object):
        """Initialization TFView object.

        Args:
            ids : tf ids object
        """
        self.ids = ids
        self.compute_obj = TFCompute(ids)

    def view_tf_coils(
        self,
        ax: plt.axes,
        select_coil=":",
        select_conductor=":",
        color="#57b6ed",
        edgecolor="#0000ff",
        facecolor="#57b6ed",
        alpha=0.7,
    ):
        """
        Plots the Toroidal Field (TF) coils on the given matplotlib axis.

        Parameters:
        ax (plt.axes): The matplotlib axis to plot on.
        select_coil (str, optional): The coil selection criteria. Defaults to ":".
        select_conductor (str, optional): The conductor selection criteria. Defaults to "".
        color (str, optional): The color to use for plotting the coils. Defaults to "#800000".

        Returns:
        Patch: A matplotlib Patch object for the TF legend.

        Notes:
        - The function retrieves TF coil data using the compute_obj's get_tf_coils method.
        - If no TF coil data is found, a warning is logged and the function returns without plotting.
        - The function plots the start and end points of the coil conductors and connects them with line segments.
        - The aspect ratio of the plot is set to be equal and the title is updated to include "tf".
        """
        coils_dict = self.compute_obj.get_tf_coils(select_coil=select_coil, select_conductor=select_conductor)

        if coils_dict is None:
            logger.warning("Can not plot, no tf coils data found.")
            return
        text_labels = []
        shapes = []
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
                if "outline" not in conductor_info:
                    # cross_sections = conductor_info["cross_section"]
                    scatter = ax.scatter(
                        elements["start_points"]["r"], elements["start_points"]["z"], color=color, s=10
                    )
                    shapes.append(scatter)
                    scatter = ax.scatter(elements["end_points"]["r"], elements["end_points"]["z"], color=color, s=10)
                    shapes.append(scatter)

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
                            shapes.append(segment)
                else:
                    # Plot cross-section contours if available
                    outline = conductor_info.get("outline", {})

                    # Convert to numpy arrays for easier manipulation
                    x1 = np.array(outline["inner"]["r"])
                    y1 = np.array(outline["inner"]["z"])
                    x2 = np.array(outline["outer"]["r"])
                    y2 = np.array(outline["outer"]["z"])

                    # Close the contour loops by appending the first point to the end
                    x1 = np.append(x1, x1[0])
                    y1 = np.append(y1, y1[0])
                    x2 = np.append(x2, x2[0])
                    y2 = np.append(y2, y2[0])

                    # Create filled polygon connecting inner and outer contours
                    x_fill = np.append(x1, x2[::-1])
                    y_fill = np.append(y1, y2[::-1])

                    # Plot contour lines
                    line1 = ax.plot(x1, y1, color=edgecolor, linewidth=1, alpha=alpha)
                    line2 = ax.plot(x2, y2, color=edgecolor, linewidth=1, alpha=alpha)
                    shapes.extend(line1)
                    shapes.extend(line2)

                    fill_patch = ax.fill(x_fill, y_fill, alpha=0.7, linewidth=0, facecolor=facecolor)
                    shapes.extend(fill_patch)

            name = ""
            if coil_info["identifier"]:
                name = coil_info["identifier"]
            elif coil_info["name"]:
                name = f"{coil_info['name']}"

            text = ax.text(cx, cy, name, fontsize="small", color="#333333", visible=False)
            text_labels.append(text)
        tf_legend = Patch(color=color, label="tf")

        ax.set_aspect("equal", adjustable="box")
        tf_legend.is_label_visible = False
        tf_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "tf" in legend.get_text():
                visible = not tf_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                tf_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, Patch) and legend.get_label() == "tf":
                visible = not tf_legend.is_shape_visible
                for scatter in shapes:
                    scatter.set_visible(visible)
                tf_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, tf")
        else:
            ax.set_title("tf")
        return tf_legend
