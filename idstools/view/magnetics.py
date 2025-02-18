"""
This module provides view functions and classes for pf_active ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import logging

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

    def view_probe(self, ax: plt.axes, show_labels=False):
        """
        Plots the positions and directions of poloidal magnetic field probes on a tokamak wall.

        Parameters:
        ax (matplotlib.axes.Axes): The matplotlib axes object where the plot will be drawn.
        show_labels (bool, optional): If True, labels for the probes will be displayed. Defaults to False.

        Returns:
        None
        """
        probe_data = self.magnetics_compute.get_probes()
        radial_coordinate = probe_data["R"]
        vertical_coordinate = probe_data["Z"]
        poloidal_angle_rad = - probe_data["Poloidal_Angle"]

        names = probe_data["Names"]
        # area = probe_data["Area"]
        # marker_size = (Area / max(Area)) * 100

        ax.scatter(radial_coordinate, vertical_coordinate, c="none", edgecolors="b", label="Bpol Probes")

        arrow_length = 0.2
        dx = arrow_length * np.cos(poloidal_angle_rad)
        dy = arrow_length * np.sin(poloidal_angle_rad)
        ax.quiver(
            radial_coordinate,
            vertical_coordinate,
            dx,
            dy,
            angles="xy",
            scale_units="xy",
            scale=1.5,
            color="blue",
            width=0.003,
        )

        lables = []
        if show_labels:
            for i, name in enumerate(names):
                if name not in lables:
                    ax.text(
                        radial_coordinate[i] + 0.01, vertical_coordinate[i], name, fontsize=8, ha="left", va="center"
                    )
                    lables.append(name)

        ax.set_xlabel("R [m]")
        ax.set_ylabel("Z [m]")
        ax.set_title("Poloidal Magnetic Field Probes on Tokamak Wall")
        ax.legend()
        ax.set_aspect("equal")
        ax.grid(True)

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
        radial_coordinate = flux_loops["R"]
        vertical_coordinate = flux_loops["Z"]

        names = flux_loops["Names"]
        # area = flux_loops["Area"]
        # marker_size = (area / max(area)) * 300  # Scale marker size
        ax.scatter(radial_coordinate, vertical_coordinate, c="none", edgecolors="r", label="flux loops")
        lables = []
        if show_labels:
            for i, name in enumerate(names):
                if name not in lables:
                    ax.text(
                        radial_coordinate[i][0] + 0.05,
                        vertical_coordinate[i][0],
                        name,
                        fontsize=8,
                        ha="left",
                        va="center",
                    )
                    lables.append(name)

        ax.set_xlabel("R [m]")
        ax.set_ylabel("Z [m]")
        ax.set_title("Flux Loops Around Tokamak Wall")
        ax.legend()
        ax.set_aspect("equal")
        ax.grid(True)


# plt.figure(figsize=(8, 8))

# # Plot tokamak boundary
# plt.plot(X_wall, Y_wall, 'k', linewidth=2, label="Tokamak Wall")

# # Scatter plot of probes
# sc = plt.scatter(R, Z, c=Poloidal_Angle, cmap="coolwarm", edgecolors='k', s=Marker_Size, label="Bpol Probes")

# # Add probe names as annotations
# for i, name in enumerate(Names):
#     plt.text(R[i] + 0.05, Z[i], name.split()[-1], fontsize=9, ha='left', va='center')

# # Colorbar for poloidal angles
# cbar = plt.colorbar(sc)
# cbar.set_label("Poloidal Angle [rad]")

# plt.xlabel("R [m]")
# plt.ylabel("Z [m]")
# plt.title("Poloidal Magnetic Field Probes on Tokamak Wall")
# plt.legend()
# plt.axis("equal")
# plt.grid(True)
# plt.show()

# if coils_dict := self.compute_obj.get_active_pf_coils():
#             for _, coil_info in coils_dict.items():
#                 coil_elements = coil_info["elements"]
#                 for _, element_info in coil_elements.items():
#                     cew, ceh, cec = (
#                         element_info["horizontal_width"],
#                         element_info["horizontal_height"],
#                         element_info["cec"],
#                     )
#                     rectangle = Rectangle(cec, cew, ceh, edgecolor="#fd7e14", facecolor="#fd7e14", alpha=0.5)

#                     ax.add_patch(rectangle)
#                     rx, ry = rectangle.get_xy()
#                     cx = rx + rectangle.get_width() / 2.0
#                     cy = ry + rectangle.get_height() / 2.0

#                     if show_labels:
#                         name = ""
#                         if coil_info["identifier"]:
#                             name = coil_info["identifier"]
#                         elif coil_info["name"]:
#                             name = f"{coil_info['name']}"

#                         ax.text(
#                             cx,
#                             cy,
#                             name,
#                             fontsize="x-small",
#                         )
#             ax.set_aspect("equal", adjustable="box")
