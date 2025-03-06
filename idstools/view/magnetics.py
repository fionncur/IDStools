"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.lines as mlines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import numpy as np

from idstools.compute.magnetics import MagneticsCompute

logger = logging.getLogger("module")


class MagneticsView:
    """This class provides view functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization MagneticsView object.

        Args:
            ids : magnetics ids object
        """
        self.ids = ids
        self.magnetics_compute = MagneticsCompute(ids)

    def view_b_field_probes(self, ax: plt.axes, probe_type="b_field_pol_probe", select=":"):
        """
        Plots the positions and directions of poloidal magnetic field probes on a tokamak wall.

        Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object where the plot will be drawn.
        probe_type (str, optional): The type of probe to plot. Defaults to "b_field_pol_probe".
        select (str, optional): Selection criteria for the probe data. Defaults to ":".

        Returns:
        None
        """
        probe_data = self.magnetics_compute.get_b_field_probes(probe_type, select=select)
        if probe_data is None or len(probe_data["r"]) == 0:
            logger.warning(f"Can not plot, no {probe_type} data found.")
            return
        if probe_type == "b_field_pol_probe":
            patch_color = "#ff3d41"
        elif probe_type == "b_field_phi_probe":
            patch_color = "#f37199"
        poloidal_angle_rad = -probe_data["poloidal_angle"]
        rect_size = 0
        arrow_length = 0.001

        text_labels = []
        shapes = []
        for i, (radial_coordinate, vertical_coordinate, poloidal_angle_rad, length, name) in enumerate(
            zip(probe_data["r"], probe_data["z"], poloidal_angle_rad, probe_data["lengths"], probe_data["names"])
        ):
            if length > 0:
                rect_size = length
                arrow_length = rect_size
            if rect_size == 0:
                scatter = ax.scatter(
                    radial_coordinate, vertical_coordinate, facecolors="none", edgecolors=patch_color, marker="s", s=20
                )
                shapes.append(scatter)
            else:
                rect_x = radial_coordinate - rect_size / 2
                rect_y = vertical_coordinate - rect_size / 2
                rect = patches.Rectangle(
                    (rect_x, rect_y),
                    rect_size,
                    rect_size,
                    edgecolor=patch_color,
                    facecolor="none",
                )
                ax.add_patch(rect)
                shapes.append(rect)

            start_x = radial_coordinate
            start_y = vertical_coordinate
            end_x = start_x + arrow_length * np.cos(poloidal_angle_rad)
            end_y = start_y + arrow_length * np.sin(poloidal_angle_rad)

            arrow = patches.FancyArrowPatch(
                (start_x, start_y),
                (end_x, end_y),
                arrowstyle="->",
                mutation_scale=10,
                color=patch_color,
                fill=False,
            )
            ax.add_patch(arrow)
            shapes.append(arrow)
            ha = "right" if i % 2 == 0 else "left"
            text = ax.text(
                radial_coordinate,
                vertical_coordinate,
                f"{name}",
                fontsize="small",
                ha=ha,
                color="#333333",
                visible=False,
            )
            text_labels.append(text)
        magnetics_legend = mlines.Line2D(
            [],
            [],
            marker="s",
            color=patch_color,
            markersize=8,
            label=f"magnetics/{probe_type}",
            fillstyle="none",
            linestyle="None",
        )
        magnetics_legend.is_label_visible = False
        magnetics_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and probe_type in legend.get_text():
                visible = not magnetics_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                magnetics_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, mlines.Line2D) and legend.get_label() == f"magnetics/{probe_type}":
                visible = not magnetics_legend.is_shape_visible
                for scatter in shapes:
                    scatter.set_visible(visible)
                magnetics_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/{probe_type}")
        else:
            ax.set_title(f"magnetics/{probe_type}")
        return magnetics_legend

    def view_flux_loop(self, ax: plt.axes, select=":", color="#ff3d41"):
        """
        Plots the flux loops on the given matplotlib axes.

        Parameters:
        ax (plt.axes): The matplotlib axes on which to plot the flux loops.

        Returns:
        None
        """
        flux_loops = self.magnetics_compute.get_flux_loops(select=select)
        if flux_loops is None or len(flux_loops["r"]) == 0:
            logger.warning("Can not plot, no flux_loop data found.")
            return
        scatter_points = []
        text_labels = []
        for index, (r, z, name) in enumerate(zip(flux_loops["r"], flux_loops["z"], flux_loops["names"])):
            points = []
            for _r, _z in zip(r, z):
                points.append((_r, _z))
            ha = "right" if index % 2 == 0 else "left"
            text = ax.text(r[0], z[0], f"{name}", fontsize="small", ha=ha, color="#333333", visible=False)
            text_labels.append(text)

            scatter = ax.scatter(r, z, edgecolors=color, c="none", marker="o", lw=1, s=50)
            scatter_points.append(scatter)
            # rectangle = patches.Polygon(points, closed=True, edgecolor=color, facecolor="none", linewidth=0.5)
            # ax.add_patch(rectangle)

        magnetics_legend = mlines.Line2D(
            [],
            [],
            marker="o",
            color=color,
            markersize=8,
            label="magnetics/flux_loop",
            fillstyle="none",
            linestyle="None",
        )
        magnetics_legend.is_label_visible = False
        magnetics_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "flux_loop" in legend.get_text():
                visible = not magnetics_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                magnetics_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, mlines.Line2D) and legend.get_label() == "magnetics/flux_loop":
                visible = not magnetics_legend.is_shape_visible
                for scatter in scatter_points:
                    scatter.set_visible(visible)
                magnetics_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/flux_loop")
        else:
            ax.set_title("magnetics/flux_loop")
        return magnetics_legend

    def view_rogowski_coil(self, ax: plt.axes, select=":", color="#ff3d41"):
        """
        Plots Rogowski coil data on the given matplotlib axes.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the Rogowski coil data.
        select (str, optional): Selection criteria for the Rogowski coil data. Defaults to ":".
        color (str, optional): Color for the Rogowski coil markers. Defaults to "#069AF3".

        Returns:
        matplotlib.lines.Line2D: A legend handle for the Rogowski coil plot.

        Logs a warning if no Rogowski coil data is found.
        """
        rogowski_coil_data = self.magnetics_compute.get_rogowski_coils(select=select)
        if rogowski_coil_data is None or len(rogowski_coil_data["r"]) == 0:
            logger.warning("Can not plot, no rogowski_coil data found.")
            return
        text_labels = []
        scatter_points = []
        for index, (r, z, name) in enumerate(
            zip(rogowski_coil_data["r"], rogowski_coil_data["z"], rogowski_coil_data["names"])
        ):
            points = []
            for _r, _z in zip(r, z):
                points.append((_r, _z))

            scatter = ax.scatter(
                r,
                z,
                c="none",
                edgecolors=color,
                marker="D",
                lw=1,
                s=50,
            )
            scatter_points.append(scatter)
            # rectangle = patches.Polygon(points, closed=True, edgecolor=color, facecolor="none")
            # ax.add_patch(rectangle)

            ha = "right" if index % 2 == 0 else "left"
            text = ax.text(r[0], z[0], f"{name}", fontsize="small", ha=ha, color="#333333", visible=False)
            text_labels.append(text)
        rogowski_legend = mlines.Line2D(
            [],
            [],
            marker="D",
            color=color,
            markersize=8,
            label="magnetics/rogowski_coil",
            fillstyle="none",
            linestyle="None",
        )
        rogowski_legend.is_label_visible = False
        rogowski_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "rogowski_coil" in legend.get_text():
                visible = not rogowski_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                rogowski_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, mlines.Line2D) and legend.get_label() == "magnetics/rogowski_coil":
                visible = not rogowski_legend.is_shape_visible
                for scatter in scatter_points:
                    scatter.set_visible(visible)
                rogowski_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/rogowski_coil")
        else:
            ax.set_title("magnetics/rogowski_legend")
        return rogowski_legend

    def view_shunt(self, ax: plt.axes, select=":", color="#ff3d41"):
        shunt_data = self.magnetics_compute.get_shunts(select=select)
        if shunt_data is None or len(shunt_data["r1"]) == 0:
            logger.warning("Can not plot, no shunt data found.")
            return

        text_labels = []
        scatter_points = []
        for index, (r1, z1, r2, z2, name) in enumerate(
            zip(shunt_data["r1"], shunt_data["z1"], shunt_data["r2"], shunt_data["z2"], shunt_data["names"])
        ):
            # points = [(r1, z1), (r2, z2)]
            scatter = ax.scatter(
                [r1, r2],
                [z1, z2],
                c="none",
                edgecolors=color,
                marker="^",
                lw=1,
                s=50,
            )
            scatter_points.append(scatter)
            # rectangle = patches.Polygon(points, closed=True, edgecolor=color, facecolor="none")
            # ax.add_patch(rectangle)

            ha = "right" if index % 2 == 0 else "left"
            text = ax.text(r1, z1, f"{name}", fontsize="small", ha=ha, color="#333333", visible=False)
            text_labels.append(text)

        shunt_legend = mlines.Line2D(
            [],
            [],
            marker="^",
            color=color,
            markersize=8,
            label="magnetics/shunt",
            fillstyle="none",
            linestyle="None",
        )
        shunt_legend.is_label_visible = False
        shunt_legend.is_shape_visible = True

        def on_legend_click(event):
            legend = event.artist
            if isinstance(legend, mtext.Text) and "shunt" in legend.get_text():
                visible = not shunt_legend.is_label_visible
                for text in text_labels:
                    text.set_visible(visible)

                shunt_legend.is_label_visible = visible
                font_weight = "bold" if visible else "normal"
                legend.set_fontweight(font_weight)
                ax.figure.canvas.draw_idle()
            elif isinstance(legend, mlines.Line2D) and legend.get_label() == "magnetics/shunt":
                visible = not shunt_legend.is_shape_visible
                for scatter in scatter_points:
                    scatter.set_visible(visible)
                shunt_legend.is_shape_visible = visible
                alpha_value = 1.0 if visible else 0.7
                legend.set_alpha(alpha_value)
                ax.figure.canvas.draw_idle()

        ax.figure.canvas.mpl_connect("pick_event", on_legend_click)

        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/shunt")
        else:
            ax.set_title("magnetics/shunt")
        return shunt_legend
