"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.lines as mlines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
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

    def view_b_field_probes(self, ax: plt.axes, probe_type="b_field_pol_probe", select=":", show_labels=False):
        """
        Plots the positions and directions of poloidal magnetic field probes on a tokamak wall.

        Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object where the plot will be drawn.
        show_labels (bool, optional): If True, labels for the probes will be displayed. Defaults to False.

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
            patch_color = "#ff3d41"
        poloidal_angle_rad = -probe_data["poloidal_angle"]
        rect_size = 0

        for i, (radial_coordinate, vertical_coordinate, poloidal_angle_rad, length, name) in enumerate(
            zip(probe_data["r"], probe_data["z"], poloidal_angle_rad, probe_data["lengths"], probe_data["names"])
        ):
            if length > 0:
                rect_size = length

            arrow_length = rect_size
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
            if show_labels:
                ax.annotate(
                    f"{name}",
                    xy=(radial_coordinate, vertical_coordinate),
                    xytext=(
                        radial_coordinate,
                        vertical_coordinate,
                    ),  # (radial_coordinate[i] + 0.2, vertical_coordinate[i] + 0.1 * (-1) ** i)
                    fontsize="small",
                    color="#333333",
                )
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
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/{probe_type}")
        else:
            ax.set_title(f"magnetics/{probe_type}")
        return magnetics_legend

    def view_flux_loop(self, ax: plt.axes, select=":", color="#ff3d41", show_labels=False):
        """
        Plots the flux loops on the given matplotlib axes.

        Parameters:
        ax (plt.axes): The matplotlib axes on which to plot the flux loops.
        show_labels (bool): If True, labels for the flux loops will be displayed. Default is False.

        Returns:
        None
        """
        flux_loops = self.magnetics_compute.get_flux_loops(select=select)
        if flux_loops is None or len(flux_loops["r"]) == 0:
            logger.warning("Can not plot, no flux_loop data found.")
            return
        for index, (r, z, name) in enumerate(zip(flux_loops["r"], flux_loops["z"], flux_loops["names"])):
            points = []
            for _r, _z in zip(r, z):
                points.append((_r, _z))
            if show_labels:
                ax.annotate(f"{name}", xy=(r[0], z[0]), xytext=(r[0], z[0]), fontsize="small", color="#333333")
            ax.scatter(r, z, edgecolors=color, c="none", marker="o", lw=1, s=50)
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
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/flux_loop")
        else:
            ax.set_title("magnetics/flux_loop")
        return magnetics_legend

    def view_rogowski_coil(self, ax: plt.axes, select=":", color="#ff3d41", show_labels=False):
        """
        Plots Rogowski coil data on the given matplotlib axes.

        Parameters:
        ax (matplotlib.axes.Axes): The axes on which to plot the Rogowski coil data.
        select (str, optional): Selection criteria for the Rogowski coil data. Defaults to ":".
        color (str, optional): Color for the Rogowski coil markers. Defaults to "#069AF3".
        show_labels (bool, optional): Whether to show labels for the Rogowski coils. Defaults to False.

        Returns:
        matplotlib.lines.Line2D: A legend handle for the Rogowski coil plot.

        Logs a warning if no Rogowski coil data is found.
        """
        rogowski_coil_data = self.magnetics_compute.get_rogowski_coils(select=select)
        if rogowski_coil_data is None or len(rogowski_coil_data["r"]) == 0:
            logger.warning("Can not plot, no rogowski_coil data found.")
            return
        for index, (r, z, name) in enumerate(
            zip(rogowski_coil_data["r"], rogowski_coil_data["z"], rogowski_coil_data["names"])
        ):
            points = []
            for _r, _z in zip(r, z):
                points.append((_r, _z))

            ax.scatter(
                r,
                z,
                c="none",
                edgecolors=color,
                marker="D",
                lw=1,
                s=50,
            )

            # rectangle = patches.Polygon(points, closed=True, edgecolor=color, facecolor="none")
            # ax.add_patch(rectangle)

            if show_labels:
                ax.annotate(f"{name}", xy=(r[0], z[0]), xytext=(r[0], z[0]), fontsize="small", color="#333333")
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
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/rogowski_coil")
        else:
            ax.set_title("magnetics/rogowski_legend")
        return rogowski_legend

    def view_shunt(self, ax: plt.axes, select=":", color="#ff3d41", show_labels=False):
        shunt_data = self.magnetics_compute.get_shunts(select=select)
        if shunt_data is None or len(shunt_data["r1"]) == 0:
            logger.warning("Can not plot, no shunt data found.")
            return

        for index, (r1, z1, r2, z2, name) in enumerate(
            zip(shunt_data["r1"], shunt_data["z1"], shunt_data["r2"], shunt_data["z2"], shunt_data["names"])
        ):
            points = [(r1, z1), (r2, z2)]
            ax.scatter(
                [r1, r2],
                [z1, z2],
                c="none",
                edgecolors=color,
                marker="^",
                lw=1,
                s=50,
            )

            rectangle = patches.Polygon(points, closed=True, edgecolor=color, facecolor="none")
            ax.add_patch(rectangle)

            if show_labels:
                ax.annotate(f"{name}", xy=(r1, z1), xytext=(r1, z1), fontsize="small", color="#333333")

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
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, magnetics/shunt")
        else:
            ax.set_title("magnetics/shunt")
        return shunt_legend
