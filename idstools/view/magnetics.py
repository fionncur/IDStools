"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np

from idstools.compute.magnetics import MagneticsCompute

logger = logging.getLogger("module")


class MagneticsView:
    """This class provides view functions for pf_active ids"""

    def __init__(self, ids: object):
        """Initialization PFActiveView object.

        Args:
            ids : pf_active ids object
        """
        self.ids = ids
        self.magnetics_compute = MagneticsCompute(ids)

    def view_b_field_pol_probes(self, ax: plt.axes, show_labels=False):
        """
        Plots the positions and directions of poloidal magnetic field probes on a tokamak wall.

        Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object where the plot will be drawn.
        show_labels (bool, optional): If True, labels for the probes will be displayed. Defaults to False.

        Returns:
        None
        """
        probe_data = self.magnetics_compute.get_b_field_pol_probes()
        poloidal_angle_rad = -probe_data["poloidal_angle"]
        rect_size = 0.2

        for i, (radial_coordinate, vertical_coordinate, poloidal_angle_rad, length, name) in enumerate(
            zip(probe_data["r"], probe_data["z"], poloidal_angle_rad, probe_data["lengths"], probe_data["identifiers"])
        ):
            if length > 0:
                rect_size = length
            arrow_length = rect_size
            rect_x = radial_coordinate - rect_size / 2
            rect_y = vertical_coordinate - rect_size / 2
            rect = patches.Rectangle(
                (rect_x, rect_y),
                rect_size,  # Width
                rect_size,  # Height
                linewidth=0.8,
                edgecolor="gray",
                facecolor="#FAEBD7",
                alpha=0.5,
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
                linewidth=0.8,
                color="darkgray",
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
                    fontsize=8,
                    # arrowprops=dict(arrowstyle="->", color="gray", lw=1),
                    textcoords="data",
                    bbox=dict(boxstyle="round,pad=0.3", fc="none", ec="gray", lw=0.5),
                    verticalalignment="bottom",  # Align text vertically
                    horizontalalignment="left",  # Align text horizontally
                )
        title = ax.get_title()
        ax.set_title(f"{title}\nb_field_pol_probes")

    def view_flux_loop(self, ax: plt.axes, show_labels=False):
        """
        Plots the flux loops on the given matplotlib axes.

        Parameters:
        ax (plt.axes): The matplotlib axes on which to plot the flux loops.
        show_labels (bool): If True, labels for the flux loops will be displayed. Default is False.

        Returns:
        None
        """
        flux_loops = self.magnetics_compute.get_flux_loops()

        for index, (r, z, name) in enumerate(zip(flux_loops["r"], flux_loops["z"], flux_loops["identifiers"])):
            points = [(r[0], z[0]), (r[1], z[1]), (r[2], z[2]), (r[3], z[3]), (r[4], z[4])]
            ax.scatter(r, z, c="none", edgecolors="darkgray", facecolor="none", marker="o", label="flux loops")

            rectangle = patches.Polygon(points, closed=True, edgecolor="lightcoral", facecolor="none")
            ax.add_patch(rectangle)

            if show_labels:
                ax.annotate(
                    f"{name}",
                    xy=(r[0], z[0]),
                    xytext=(r[0], z[0]),
                    fontsize=8,
                    # arrowprops=dict(arrowstyle="->", color="gray", lw=1),
                    textcoords="data",
                    bbox=dict(boxstyle="round,pad=0.3", fc="none", ec="gray", lw=0.5),
                    verticalalignment="bottom",
                    horizontalalignment="left",
                )
        ax.set_xlim(-5, 20)
        title = ax.get_title()
        ax.set_title(f"{title}  \nflux_loop")
