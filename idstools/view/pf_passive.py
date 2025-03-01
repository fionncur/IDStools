"""
This module provides view functions and classes for pf_passive ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, FancyArrow, Patch, Polygon, Rectangle, Wedge

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

    def view_pf_passive_loops(
        self,
        ax: plt.axes,
        select=":",
        edgecolor="#52bf90",
        facecolor="#52bf90",
        alpha=0.7,
        linewidth=1,
        show_labels=False,
    ):
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
        loops_dict = self.compute_obj.get_pf_passive_loops(select=select)
        if loops_dict is None:
            logger.warning("Can not plot, no pf passive loops data found.")
            return
        for _, loop_info in loops_dict.items():
            loop_elements = loop_info["elements"]
            name = loop_info["name"]

            for _, element_info in loop_elements.items():
                cx = cy = 0.0
                if element_info["geometry_type"] == 2:
                    width = element_info["width"]
                    height = element_info["height"]
                    r, z = (
                        element_info["r"],
                        element_info["z"],
                    )
                    lower_left_x = r - width / 2
                    lower_left_y = z - height / 2
                    rectangle = Rectangle(
                        (lower_left_x, lower_left_y),
                        width,
                        height,
                        edgecolor=edgecolor,
                        facecolor=facecolor,
                        alpha=alpha,
                    )
                    ax.add_patch(rectangle)
                    rx, ry = rectangle.get_xy()
                    cx = rx + rectangle.get_width() / 2.0
                    cy = ry + rectangle.get_height() / 2.0
                elif element_info["geometry_type"] == 3:
                    r = element_info["r"]
                    z = element_info["z"]
                    length_alpha = element_info["length_alpha"]
                    length_beta = element_info["length_beta"]
                    alpha = element_info["alpha"]
                    beta = element_info["beta"]

                    corner1 = np.array([r, z])

                    corner2 = corner1 + np.array([length_alpha * np.cos(alpha), length_alpha * np.sin(alpha)])

                    corner3 = corner2 + np.array(
                        [length_beta * np.cos(0.5 * np.pi + beta), length_beta * np.sin(0.5 * np.pi + beta)]
                    )
                    corner4 = corner1 + np.array(
                        [length_beta * np.cos(0.5 * np.pi + beta), length_beta * np.sin(0.5 * np.pi + beta)]
                    )

                    parallelogram = np.array([corner1, corner2, corner3, corner4, corner1])

                    parallelogram_patch = Polygon(
                        parallelogram, closed=True, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidth=1
                    )

                    ax.add_patch(parallelogram_patch)

                    cx = np.mean(parallelogram[:, 0])
                    cy = np.mean(parallelogram[:, 1])
                elif element_info["geometry_type"] == 4:

                    r = element_info["r"]
                    z = element_info["z"]
                    curvature_radii = element_info["curvature_radii"]

                    radius, start_angle, end_angle = curvature_radii

                    arc = Arc(
                        (r, z),
                        2 * radius,
                        2 * radius,
                        angle=0,
                        theta1=start_angle,
                        theta2=end_angle,
                        edgecolor=edgecolor,
                        facecolor=facecolor,
                        alpha=alpha,
                        linewidth=1,
                    )
                    ax.add_patch(arc)
                    mid_angle = (start_angle + end_angle) / 2
                    cx = r + radius * np.cos(np.radians(mid_angle))
                    cy = z + radius * np.sin(np.radians(mid_angle))
                elif element_info["geometry_type"] == 5:

                    r = element_info["r"]
                    z = element_info["z"]
                    radius_inner = element_info["radius_inner"]
                    radius_outer = element_info["radius_outer"]

                    outer_wedge = Wedge(
                        (r, z), radius_outer, 0, 360, edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidth=1
                    )
                    inner_wedge = Wedge(
                        (r, z), radius_inner, 0, 360, edgecolor=edgecolor, facecolor="w", alpha=1, linewidth=1
                    )

                    ax.add_patch(outer_wedge)
                    ax.add_patch(inner_wedge)
                elif element_info["geometry_type"] == 6:
                    thickness = element_info["thickness"]
                    r1 = element_info["r1"]
                    z1 = element_info["z1"]
                    r2 = element_info["r2"]
                    z2 = element_info["z2"]
                    line = FancyArrow(
                        r1,
                        z1,
                        r2 - r1,
                        z2 - z1,
                        width=thickness,
                        head_length=0,
                        head_width=0,
                        color=facecolor,
                        alpha=alpha,
                        linewidth=1,
                    )
                    ax.add_patch(line)
                    cx = (r1 + r2) / 2
                    cy = (z1 + z2) / 2
                elif element_info["geometry_type"] == 1 or len(element_info["r"]) != 0:
                    r = element_info["r"]
                    z = element_info["z"]
                    if len(r) == 1:
                        ax.scatter(r, z, color="steelblue")
                    else:
                        outline = Polygon(
                            list(zip(r, z)),
                            closed=True,
                            edgecolor=edgecolor,
                            facecolor="none",
                            alpha=alpha,
                            linewidth=1,
                        )
                        ax.add_patch(outline)
                    cx = np.mean(r)
                    cy = np.mean(z)
                if show_labels:
                    name = ""
                    if loop_info["identifier"]:
                        name = loop_info["identifier"]
                    elif loop_info["name"]:
                        name = f"{loop_info['name']}"

                    ax.text(cx, cy, name, fontsize="small", color="#333333")
        pf_passive_legend = Patch(
            edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidth=linewidth, label="pf_passive"
        )

        ax.set_aspect("equal", adjustable="box")
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, pf_passive")
        else:
            ax.set_title("pf_passive")
        return pf_passive_legend
