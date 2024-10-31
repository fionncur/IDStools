"""
This module provides view functions and classes for equilibrium ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`_.

"""

import copy
import logging

import imaspy as imas
import matplotlib.pyplot as plt
import numpy as np

from idstools.compute.equilibrium import EquilibriumCompute
from idstools.view.common import BasePlot

logger = logging.getLogger("module")


class EquilibriumView(BasePlot):
    def __init__(self, ids: object):
        """
        This is a constructor function that initializes an object with an input object and creates
        another object using the input object.

        Args:
            ids (object): The parameter `ids` is an object that is being passed to the constructor
                of the class. It is not clear from the code snippet what type of object it is, but it is being
                stored as an instance variable `self.ids`.
        """
        self.ids = ids
        self.compute_obj = EquilibriumCompute(ids)

    def view_magnetic_poloidal_flux(
        self,
        ax: plt.axes,
        time_slice: int,
        profiles2d_index: int = 0,
        plot_rho: bool = False,
    ):
        """
        This function plots the magnetic poloidal flux contours on a 2D Cartesian grid.

        Args:
            ax: `ax` is a matplotlib axis object on which the magnetic poloidal flux contour plot will be drawn.

        Example:
            .. code-block:: python

                import imaspy as imas
                from idstools.view.equilibrium import EquilibriumView
                from idstools.view.common import PlotCanvas

                connection = imas.DBEntry("imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3","r")
                connection.open()
                idsObj = connection.get('equilibrium')

                canvas = PlotCanvas(1, 1) # create canvas
                ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

                viewObj = EquilibriumView(idsObj)
                viewObj.viewMagneticPoloidalFlux(ax) # plot contour on the canvas axes

                ax.set_title("uri=imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3")
                ax.plot()
                canvas.show()

            .. thumbnail:: /_static/images/EquilibriumView_viewMagneticPoloidalFlux.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.compute.equilibrium.EquilibriumCompute.get2DCartesianGrid`
            :func:`idstools.compute.equilibrium.EquilibriumCompute.getRho2D`

            :meth:`plotIP`
        """
        cartestion_grid = self.compute_obj.get2d_cartesian_grid(time_slice, profiles2d_index)
        if cartestion_grid is not None:
            levels = 30
            if plot_rho:
                rho2d = self.compute_obj.get_rho2d(time_slice)
                if rho2d is not None:
                    ax.contour(
                        cartestion_grid["r2d"],
                        cartestion_grid["z2d"],
                        rho2d,
                        levels,
                        colors="r",
                    )
            ax.contour(
                cartestion_grid["r2d"],
                cartestion_grid["z2d"],
                cartestion_grid["psi2d"],
                levels,
            )
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("$R$ [m]")
            ax.set_ylabel("$Z$ [m]")
            # ax.set_xlim(3.4, cartestionGrid["r2d"].max())
            # ax.set_ylim(cartestionGrid["z2d"].min() * 0.7, cartestionGrid["z2d"].max() * 0.7)
            ax.tick_params(axis="both", which="major")

    def view_pulse_info(self, ax: plt.axes, title: str, hostdir: str, shot: int, run: int, t: float):
        self.database_info(ax, title, hostdir, shot, run, t)

    def plot_ip(self, ax):
        """
        This function plots the plasma current over time on a given axis.

        Args:
            ax: The parameter "ax" is a matplotlib axis object.
        """
        plasma_current = self.compute_obj.get_ip()
        time_array = self.ids.time
        if len(plasma_current) <= 3:
            ax.plot(time_array, plasma_current, color="b", marker="o", label="$I_p$ [MA]")
        else:
            ax.plot(time_array, plasma_current, color="b", label="$I_p$ [MA]")
        if len(time_array) != 1:
            ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(plasmaCurrent)*1.2)
        ax.legend(
            bbox_to_anchor=(1.0, 0.5),
            loc="center left",
            borderaxespad=0.0,
            frameon=False,
            fontsize="x-small",
        )
        ax.set_ylim(0, 20)

    def plot_poloidal_equilibrium(self, ax, time_slice: int):
        """
        This function plots a poloidal equilibrium contour plot using flux surface quantities extracted from the
        equilibrium.

        Args:
            ax: `ax` is a matplotlib axis object.
            timeSlice (int): timeSlice is an integer index.

        Returns:
            the contour plot object `cntr`.
        """
        # Extract flux surface quantities from equilibrium
        data = self.compute_obj.get_flux_surfaces(time_slice)
        r2d = data["r2d"]
        z2d = data["z2d"]
        # rho2d = data["rho2d"]
        psi2d = data["psi2d"]
        cntr = ax.contour(r2d, z2d, psi2d, 50, cmap="summer")
        # if len(rho2d)>0:
        #    cntr = ax_polview.contour(r2d,z2d,rho2d,50,cmap='YlOrBr')

        # ax_polview.set_xlim(r2d.min(),r2d.max())
        ax.set_xlim(3.4, r2d.max())
        ax.set_ylim(z2d.min() * 0.7, z2d.max() * 0.7)
        ax.set_aspect("equal", adjustable="box")

        return cntr

    def plot_topplotequilibrium(self, ax, time_slice, label="Plasma Boundaries"):
        """
        This function plots the top view equilibrium of a plasma and updates the plot if specified.

        Args:
            ax: `ax` is a matplotlib axis object.
            time_slice: The time index is an integer

        Returns:
            list containing two plot objects: ax_topview_plot_eq1 and ax_topview_plot_eq2.
        """
        # TODO: Refactor update mechanism of the plot
        data = self.compute_obj.get_top_view(time_slice)
        bndcolor = "chocolate"
        colorcounter = 0

        if colorcounter == 1:
            ax.plot(
                data["xpla"],
                data["ypla"],
                color=bndcolor,
                label=label,
            )
        else:
            ax.plot(data["xpla"], data["ypla"], color=bndcolor)
        ax.plot(data["xplap"], data["yplap"], color=bndcolor)
        ax.set_xlim((-data["r0"] - data["amin"]) * 1.1, (data["r0"] + data["amin"]) * 1.1)
        ax.set_aspect("equal", adjustable="box")

    def plotequilibrium(self, ax, time_slice):
        quantities = self.compute_obj.get2d_cartesian_grid(time_slice)
        if quantities is not None:
            r2d, z2d, psi2d = (
                quantities["r2d"],
                quantities["z2d"],
                quantities["psi2d"],
            )
            ax.xaxis.tick_top()
            ax.xaxis.set_label_position("top")

            ax.contour(r2d, z2d, psi2d, 50)  # ,label=r'$\Psi_{pol}$')
            ax.set_xlim(r2d.min(), r2d.max())
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("R (m)")
            ax.set_ylabel("Z (m)")

            ax.set_xlabel("$R\\/\\mathrm{[m]}$")
            # ax.tick_params(axis='both',which='major',labelsize=ticksize)
            ax.set_ylabel(r"$Z\/\mathrm{[m]}$")
            # ax.tick_params(
            #     axis="x", which="both", bottom=False, top=False, labelbottom=False
            # )
            ax.set_title("2D equilibrium")
        else:
            ax.text(0.2, 0.5, "2D equilibrium", fontsize=10)
            ax.text(0.2, 0.45, "not available", fontsize=10)

    def plot_profiles_1d_quantities(self, axes_list, time_slice, attributes=None):
        quantities = self.compute_obj.get_profiles_1d_quantities(time_slice, attributes)
        if not quantities:
            return
        counter = 0
        for name, field in quantities.items():
            if field.has_value:
                copied_field = copy.deepcopy(field)

                if isinstance(copied_field.value, np.floating) or isinstance(copied_field.value, np.ndarray):
                    copied_field[copied_field == imas.ids_defs.EMPTY_FLOAT] = np.nan
                if np.all(np.isnan(copied_field.value)):
                    axes_list[counter].remove()
                    continue
                coordinate = copied_field.coordinates[0]
                axes_list[counter].plot(
                    coordinate, copied_field, label=f"{field.metadata.name} ({field.metadata.units})"
                )
                axes_list[counter].set_xlabel(f"{coordinate.metadata.name} ({coordinate.metadata.units})")
                axes_list[counter].set_ylabel(name)
                axes_list[counter].legend(loc="upper right")
            else:
                logger.warning(f"attribute {name} is empty")
                axes_list[counter].remove()
            counter = counter + 1

    def plot_global_quantities(self, axes_list, time_slice, attributes=None):
        quantities = self.compute_obj.get_global_quantities(time_slice, attributes)
        if not quantities:
            return
        counter = 0
        for name, field in quantities.items():
            if isinstance(field["node"], np.floating) or isinstance(field["node"], np.ndarray):
                field["node"][field["node"] == imas.ids_defs.EMPTY_FLOAT] = np.nan
            if np.all(np.isnan(field["node"])):
                axes_list[counter].remove()
            else:
                axes_list[counter].plot(field["coordinate"], field["node"], label=f"{name} ({field['unit']})")
                axes_list[counter].set_xlabel(f"{field['coordinate_name']} ({field['coordinate_unit']})")
                axes_list[counter].set_ylabel(name)
                self.view_time_line(axes_list[counter], time_slice)
                axes_list[counter].legend(loc="upper right")
            counter = counter + 1

    def view_time_line(self, ax, time):
        """
        The function `view_time_line` plots a vertical dashed line on a given matplotlib axis at a specified time.

        Args:
            ax: The parameter "ax" is a reference to the second y-axis of a matplotlib figure. It is used to plot
                the timeline on the same figure as the other data.
            time: The "time" parameter is the value at which you want to plot a vertical line on the timeline. It
                represents the specific point in time that you want to highlight on the timeline.
        """
        ymin, ymax = ax.get_ylim()
        ax.plot(
            [time, time],
            [ymin, ymax],
            color="gray",
            linestyle="--",
            linewidth=1,
            label=r"$t_{slice}$",
        )
        # ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        ax.set_ylim(ymin, ymax)

    def show_info_on_plot(self, ax, info: str = "", location="right"):
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()

        ax.text(
            (xmax) + 0.2,
            (ymax / 4) + 0.01,
            info,
            verticalalignment="center",
            rotation="vertical",
            fontsize=6,
        )
