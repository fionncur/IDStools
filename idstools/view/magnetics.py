"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.lines as mlines
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path

from idstools.compute.magnetics import MagneticsCompute

logger = logging.getLogger("module")


def shunt_marker():
    return Path(
        [
            (0, 0),
            (0.2, 0),
            (0.2, 0.1),
            (0.4, 0.1),
            (0.4, 0),
            (0.6, 0),
            (0.6, -0.1),
            (0.4, -0.1),
            (0.4, -0.2),
            (0.2, -0.2),
            (0.2, -0.1),
            (0, -0.1),
            (0, 0),
        ],
        closed=True,
    )


def coil_marker():
    vertices = []
    codes = []
    num_turns = 3
    num_points_per_turn = 10

    for i in range(num_turns * num_points_per_turn + 1):
        t = i / (num_turns * num_points_per_turn)
        x = t * 2
        y = np.sin(t * 2 * np.pi * num_turns)
        vertices.append((x, y))
        if i == 0:
            codes.append(Path.MOVETO)
        else:
            codes.append(Path.LINETO)

    return Path(vertices, codes)


class MagneticsView:
    """This class provides view functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization MagneticsView object.

        Args:
            ids : magnetics ids object
        """
        self.ids = ids
        self.magnetics_compute = MagneticsCompute(ids)

    def view_b_field_probes(self, ax: plt.axes, probe_type="b_field_pol_probe", show_labels=False):
        """
        Plots the positions and directions of poloidal magnetic field probes on a tokamak wall.

        Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object where the plot will be drawn.
        show_labels (bool, optional): If True, labels for the probes will be displayed. Defaults to False.

        Returns:
        None
        """
        probe_data = self.magnetics_compute.get_b_field_probes(probe_type)
        if probe_data is None:
            logger.warning(f"Can not plot, no {probe_type} data found.")
            return
        if probe_type == "b_field_pol_probe":
            patch_color = "teal"
        elif probe_type == "b_field_phi_probe":
            patch_color = "#FAEBD7"
        poloidal_angle_rad = -probe_data["poloidal_angle"]
        rect_size = min(probe_data["lengths"])

        for i, (radial_coordinate, vertical_coordinate, poloidal_angle_rad, length, name) in enumerate(
            zip(probe_data["r"], probe_data["z"], poloidal_angle_rad, probe_data["lengths"], probe_data["names"])
        ):
            if length > 0:
                rect_size = length
            else:
                logger.warning(f"Probe {name} has a no length provided. Using default length of {rect_size}.")

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
                    fontsize="x-small",
                    color=patch_color,
                )
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, {probe_type}")
        else:
            ax.set_title(f"{probe_type}")

    def view_flux_loop(self, ax: plt.axes, select=":", show_labels=False):
        """
        Plots the flux loops on the given matplotlib axes.

        Parameters:
        ax (plt.axes): The matplotlib axes on which to plot the flux loops.
        show_labels (bool): If True, labels for the flux loops will be displayed. Default is False.

        Returns:
        None
        """
        flux_loops = self.magnetics_compute.get_flux_loops(select=select)
        if flux_loops is None:
            logger.warning("Can not plot, no flux_loop data found.")
            return
        for index, (r, z, name) in enumerate(zip(flux_loops["r"], flux_loops["z"], flux_loops["names"])):
            points = []
            for _r, _z in zip(r, z):
                points.append((_r, _z))
            if show_labels:
                ax.annotate(f"{name}", xy=(r[0], z[0]), xytext=(r[0], z[0]), fontsize="small", color="#FF6347")
            ax.scatter(r, z, edgecolors="#FF6347", c="none", marker="o", lw=1, s=50)
            # rectangle = patches.Polygon(points, closed=True, edgecolor="#FF6347", facecolor="none", linewidth=0.5)
            # ax.add_patch(rectangle)

        magnetics_legend = mlines.Line2D(
            [],
            [],
            marker="o",
            color="#FF6347",
            markersize=8,
            label="magnetics/flux_loop",
            fillstyle="none",
            linestyle="None",
        )
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, flux_loop")
        else:
            ax.set_title("flux_loop")
        return magnetics_legend

    def view_rogowski_coil(self, ax: plt.axes, show_labels=False):
        rogowski_coil_data = self.magnetics_compute.get_rogowski_coils()
        if rogowski_coil_data is None:
            logger.warning("Can not plot, no rogowski_coil data found.")
            return
        coil = coil_marker()
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
                edgecolors="darkolivegreen",
                facecolor="darkolivegreen",
                marker=coil,
                label="rogowski_coils",
                s=300,
            )

            rectangle = patches.Polygon(points, closed=True, edgecolor="darkolivegreen", facecolor="none")
            ax.add_patch(rectangle)

            if show_labels:
                ax.annotate(f"{name}", xy=(r[0], z[0]), xytext=(r[0], z[0]), fontsize="x-small", color="darkolivegreen")
        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, rogowski_coil")
        else:
            ax.set_title("rogowski_coil")

    def view_shunt(self, ax: plt.axes, show_labels=False):
        shunt_data = self.magnetics_compute.get_shunts()
        if shunt_data is None:
            logger.warning("Can not plot, no shunt data found.")
            return
        shuntm = shunt_marker()
        for index, (r1, z1, r2, z2, name) in enumerate(
            zip(shunt_data["r1"], shunt_data["z1"], shunt_data["r2"], shunt_data["z2"], shunt_data["names"])
        ):
            points = [(r1, z1), (r2, z2)]
            ax.scatter(
                [r1, r2],
                [z1, z2],
                c="none",
                edgecolors="orange",
                facecolor="crimson",
                marker=shuntm,
                label="shunt",
                s=200,
            )

            rectangle = patches.Polygon(points, closed=True, edgecolor="orange", facecolor="none")
            ax.add_patch(rectangle)

            if show_labels:
                ax.annotate(f"{name}", xy=(r1, z1), xytext=(r1, z1), fontsize="x-small", color="darkolivegreen")

        title = ax.get_title()
        if title:
            ax.set_title(f"{title}, shunt")
        else:
            ax.set_title("shunt")
