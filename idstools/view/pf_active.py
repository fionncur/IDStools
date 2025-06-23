"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.pyplot as plt
import matplotlib.text as mtext
import numpy as np
from matplotlib.patches import Arc, FancyArrow, Patch, Polygon, Rectangle, Wedge

from idstools.compute.pf_active import PfActiveCompute

logger = logging.getLogger("module")


class PFActiveView:
    """This class provides view functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization PFActiveView object.

        Args:
            ids : pf_active ids object
        """
        self.ids = ids
        self.compute_obj = PfActiveCompute(ids)

    def view_active_pf_coils(
        self,
        ax: plt.axes,
        select=":",
        edgecolor="#ff0000",
        facecolor="#ff7400",
        alpha=0.7,
    ):
        """
        This function plots and annotates the active PF coils on a existing plot.

        Args:
            ax (plt.axes): `ax` is a parameter of type `plt.axes`, It is used to add patches (such as rectangles)
                and annotations to the plot.

        Example:
            .. code-block:: python

                import imas
                from idstools.view.pf_active import PFActiveView
                from idstools.view.common import PlotCanvas

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=135005;run=4;database=ITER;version=3", "r")
                connection.open()
                idsObj = connection.get('pf_active')
                connection.close()
                canvas = PlotCanvas(1, 1) # create canvas
                ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

                viewObj = PFActiveView(idsObj)
                viewObj.viewActivePfCoils(ax, showLabels=True) # plot contour on the canvas axes

                ax.plot()
                canvas.show()

            .. image:: /_static/images/PFActiveView_viewActivePfCoils.png
                :alt: image not found
                :align: center
        """
        coils_dict = self.compute_obj.get_active_pf_coils(select=select)
        if coils_dict is None:
            logger.warning("Can not plot, no pf passive loops data found.")
            return
        text_labels = []
        shapes = []
        for cindex, coil_info in coils_dict.items():

            coil_elements = coil_info["elements"]

            name = coil_info["name"]
            cx = cy = 0.0
            for eindex, element_info in coil_elements.items():

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
                        linewidth=1,
                    )
                    ax.add_patch(rectangle)
                    shapes.append(rectangle)
                    rx, ry = rectangle.get_xy()
                    cx = rx + rectangle.get_width() / 2.0
                    cy = ry + rectangle.get_height() / 2.0
                elif element_info["geometry_type"] == 3:
                    r = element_info["r"]
                    z = element_info["z"]
                    length_alpha = element_info["length_alpha"]
                    length_beta = element_info["length_beta"]
                    geometry_alpha = element_info["alpha"]
                    geometry_beta = element_info["beta"]

                    corner1 = np.array([r, z])

                    corner2 = corner1 + np.array(
                        [length_alpha * np.cos(geometry_alpha), length_alpha * np.sin(geometry_alpha)]
                    )

                    corner3 = corner2 + np.array(
                        [
                            length_beta * np.cos(0.5 * np.pi + geometry_beta),
                            length_beta * np.sin(0.5 * np.pi + geometry_beta),
                        ]
                    )
                    corner4 = corner1 + np.array(
                        [
                            length_beta * np.cos(0.5 * np.pi + geometry_beta),
                            length_beta * np.sin(0.5 * np.pi + geometry_beta),
                        ]
                    )

                    parallelogram = np.array([corner1, corner2, corner3, corner4, corner1])

                    parallelogram_patch = Polygon(
                        parallelogram,
                        closed=True,
                        edgecolor=edgecolor,
                        facecolor=facecolor,
                        alpha=alpha,
                        linewidth=1,
                    )

                    ax.add_patch(parallelogram_patch)
                    shapes.append(parallelogram_patch)
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
                    shapes.append(arc)
                    mid_angle = (start_angle + end_angle) / 2
                    cx = r + radius * np.cos(np.radians(mid_angle))
                    cy = z + radius * np.sin(np.radians(mid_angle))
                elif element_info["geometry_type"] == 5:

                    r = element_info["r"]
                    z = element_info["z"]
                    radius_inner = element_info["radius_inner"]
                    radius_outer = element_info["radius_outer"]

                    outer_wedge = Wedge(
                        (r, z),
                        radius_outer,
                        0,
                        360,
                        edgecolor=edgecolor,
                        facecolor=facecolor,
                        alpha=alpha,
                        linewidth=1,
                    )
                    inner_wedge = Wedge((r, z), radius_inner, 0, 360, edgecolor=edgecolor, facecolor="w", alpha=alpha)

                    ax.add_patch(outer_wedge)
                    ax.add_patch(inner_wedge)
                    shapes.append(outer_wedge)
                    shapes.append(inner_wedge)
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
                    )
                    ax.add_patch(line)
                    shapes.append(line)
                    cx = (r1 + r2) / 2
                    cy = (z1 + z2) / 2
                elif element_info["geometry_type"] == 1 or len(element_info["r"]) != 0:
                    r = element_info["r"]
                    z = element_info["z"]
                    if len(r) == 1:
                        scatter = ax.scatter(r, z, color=facecolor)
                        shapes.append(scatter)
                    else:
                        outline = Polygon(
                            list(zip(r, z)),
                            closed=True,
                            edgecolor=facecolor,
                            facecolor="none",
                            alpha=alpha,
                        )
                        ax.add_patch(outline)
                        shapes.append(outline)
                    cx = np.mean(r)
                    cy = np.mean(z)
            name = ""
            if coil_info["identifier"]:
                name = coil_info["identifier"]
            elif coil_info["name"]:
                name = f"{coil_info['name']}"
            ha = "right" if cindex % 2 == 0 else "left"
            text = ax.text(cx, cy, name, fontsize="small", ha=ha, color="#333333", visible=False)
            text_labels.append(text)
        pf_active_legend = Patch(edgecolor=edgecolor, facecolor=facecolor, alpha=alpha, linewidth=1, label="pf_active")

        ax.set_aspect("equal", adjustable="box")
        pf_active_legend.is_label_visible = False
        pf_active_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "pf_active" in legend.get_text():
                visible = not pf_active_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                pf_active_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, Patch) and legend.get_label() == "pf_active":
                visible = not pf_active_legend.is_shape_visible
                for scatter in shapes:
                    scatter.set_visible(visible)
                pf_active_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, pf_active")
        else:
            ax.set_title("pf_active")
        return pf_active_legend
