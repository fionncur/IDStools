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
        self.equilibria = None

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

            .. image:: /_static/images/EquilibriumView_viewMagneticPoloidalFlux.png
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
            time_slice (int): time_slice is an integer index.

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
                coordinate = coordinate_normalized = copied_field.coordinates[0]
                if coordinate.metadata.name == "psi":
                    psi = coordinate
                    psi_min = psi[0]
                    psi_max = psi[-1]
                    coordinate_normalized = (psi - psi_min) / (psi_max - psi_min)

                axes_list[counter].plot(
                    coordinate_normalized, copied_field, label=f"{field.metadata.name} ({field.metadata.units})"
                )
                if coordinate.metadata.name == "psi":
                    axes_list[counter].set_xlabel(f"{coordinate.metadata.name} (normalized)")
                else:
                    axes_list[counter].set_xlabel(f"{coordinate.metadata.name} ({coordinate.metadata.units})")
                axes_list[counter].set_ylabel(name)
                axes_list[counter].legend(loc="upper right")
                counter = counter + 1

    def plot_global_quantities(self, axes_list, time_slice, attributes=None):
        quantities = self.compute_obj.get_global_quantities(time_slice, attributes)
        if not quantities:
            return
        counter = 0
        for name, field in quantities.items():
            if isinstance(field["node"], np.floating) or isinstance(field["node"], np.ndarray):
                field["node"][field["node"] == imas.ids_defs.EMPTY_FLOAT] = np.nan
            if field["has_value"]:
                if len(field["node"]) < 5:
                    axes_list[counter].scatter(field["coordinate"], field["node"], label=f"{name} ({field['unit']})")
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

    def _get_profile(self, jtor2D, z, time_index1, jtor2DE=None, zE=None, time_index2=None):
        #
        #  sets up parameters for the profile plot on the mid-plane
        #
        new_y11 = None
        new_y12 = None
        y_min = +1e80
        y_max = -1e80

        #  work out index for mid-plane (z=0), or thereabouts...
        targetZValue = 0
        diff = np.abs(z - targetZValue)
        k = np.argmin(diff)
        if zE is not None:
            diff = np.abs(zE - targetZValue)
            kE = np.argmin(diff)

        try:
            new_y11 = jtor2D[time_index1, :, k]
            y_min = new_y11.min()
            y_max = new_y11.max()
        except Exception as _:  # noqa: F841
            pass
        try:
            new_y12 = jtor2DE[time_index2, :, kE]
            y_min = min(y_min, new_y12.min())
            y_max = max(y_max, new_y12.max())
        except Exception as _:  # noqa: F841
            pass

        delta = (y_max - y_min) * 0.03
        y_min -= delta
        y_max += delta
        yabs = max(abs(y_max), abs(y_min))
        if yabs < 1e-3:
            scal = 1e-3
            scalStr = "m"
        elif yabs < 1e3:
            scal = 1
            scalStr = ""
        elif yabs < 1e6:
            scal = 1e3
            scalStr = "k"
        else:
            scal = 1e6
            scalStr = "M"
        if new_y11 is not None:
            new_y11 /= scal
        if new_y12 is not None:
            new_y12 /= scal
        y_min /= scal
        y_max /= scal
        return new_y12, new_y11, y_min, y_max, scalStr

    def view_profile_plot(self, ax, time_index1, equilibrium2_ids=None, time_index2=None):
        if self.equilibria is None:
            self.equilibria = self.compute_obj.get_equilibria()
            data = self.equilibria
        else:
            data = self.equilibria
        data2 = None
        if equilibrium2_ids is not None:
            compute_obj2 = EquilibriumCompute(equilibrium2_ids)
            data2 = compute_obj2.get_equilibria()
            nameE = data2["name"]
            jtor2DE = data2["jtor2D"]
            rE = data2["r"]
            zE = data2["z"]
        name = data["name"]
        jtor2D = data["jtor2D"]
        r = data["r"]
        z = data["z"]
        if data2:
            new_y12, new_y11, y_min, y_max, scaleStr = self._get_profile(
                jtor2D, z, time_index1, jtor2DE, zE, time_index2
            )
            (line12,) = ax.plot([], color="blue", label=" ")

            line12.set_label(nameE + " [$run_2$]")

            if rE is not None and new_y12 is not None:
                line12.set_xdata(rE)
                line12.set_ydata(new_y12)
        else:
            new_y12, new_y11, y_min, y_max, scaleStr = self._get_profile(jtor2D, z, time_index1)

        (line11,) = ax.plot([], color="green", label=" ")
        line11.set_label(name + " [$run_1$]")
        if r is not None and new_y11 is not None:
            line11.set_xdata(r)
            line11.set_ydata(new_y11)
            ax.set_xlim([min(r), max(r)])
            ax.set_ylim([y_min, y_max])

        ax.set_ylim(y_min, y_max)
        ax.set_ylabel("$" + scaleStr + "A/m^2$")
        ax.set_title("$J_{tor}$(mid-plane)")
        ax.set_xlabel("R [m]")
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), fancybox=True, shadow=True, ncol=2)

    def view_equlibrium_plot(self, ax, time_index1, equilibrium2_ids=None):
        if self.equilibria is None:
            self.equilibria = self.compute_obj.get_equilibria()
            data = self.equilibria
        else:
            data = self.equilibria
        data2 = None
        if equilibrium2_ids:
            self.compute_obj2 = EquilibriumCompute(equilibrium2_ids)
            data2 = self.compute_obj2.get_equilibria()
            timeE = data["time"]
            psi2DE = data2["psi2D"]
            rbE = data2["rb"]
            zbE = data2["zb"]
            rE = data2["r"]
            zE = data2["z"]
            psi_axisE = data["psi_axis"]
            psi_boundaryE = data["psi_boundary"]
        time = data["time"]
        psi2D = data["psi2D"]
        rb = data["rb"]
        zb = data["zb"]
        r = data["r"]
        z = data["z"]
        psi_axis = data["psi_axis"]
        psi_boundary = data["psi_boundary"]

        if data2:
            c, cE = self.compute_obj.get_contour(
                psi_axis, psi_boundary, time, time_index1, psi_axis2=psi_axisE, psi_boundary2=psi_boundaryE, time2=timeE
            )
        else:
            c, cE = self.compute_obj.get_contour(psi_axis, psi_boundary, time, time_index1)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Poloidal Flux")
        ax.set_xlabel("R[m]")
        ax.set_ylabel("Z[m]")
        if np.min(psi2D[time_index1]) < np.max(psi2D[time_index1]):
            ax.contour(r, z, np.transpose(psi2D[time_index1]), colors="green", levels=c, linewidths=0.85)
            (lineb1,) = ax.plot([], linewidth=2, color="green")
            lineb1.set_xdata(rb[time_index1])
            lineb1.set_ydata(zb[time_index1])
        if data2:
            if np.min(psi2DE[time_index1]) < np.max(psi2DE[time_index1]):
                time_index2 = np.argmin(abs(timeE - time[time_index1]))
                ax.contour(rE, zE, np.transpose(psi2DE[time_index2]), colors="blue", levels=cE, linewidths=0.85)
                (lineb2,) = ax.plot([], linewidth=2, color="blue")
                lineb2.set_xdata(rbE[time_index1])
                lineb2.set_ydata(zbE[time_index1])

    def view_current_plot(self, ax, time_index1, equilibrium2_ids=None):
        if self.equilibria is None:
            self.equilibria = self.compute_obj.get_equilibria()
            data = self.equilibria
        else:
            data = self.equilibria
        data2 = None
        if equilibrium2_ids:
            self.compute_obj2 = EquilibriumCompute(equilibrium2_ids)
            data2 = self.compute_obj2.get_equilibria()
            timeE = data["time"]
            ipE = data2["ip"]
        time = data["time"]
        ip = data["ip"]
        (line31,) = ax.plot([], marker="x", color="green")
        (line32,) = ax.plot([], marker="x", color="blue")
        line33 = ax.axvline(color="red", linestyle="--")
        ax.set_title("$I_p$")
        ax.set_xlabel("t [s]")
        ax.set_ylabel("MA")
        ylims = ax.get_ylim()
        line33.set_xdata([time[time_index1]])
        ax.set_ylim(ylims)
        line31.set_xdata(time)
        line31.set_ydata(ip / 1e6)
        xlims = np.array([min(time), max(time)])
        ylims = np.array([min(ip), max(ip)]) / 1e6
        if data2 is not None:
            line32.set_xdata(timeE)
            line32.set_ydata(ipE / 1e6)
            xlims[0] = np.minimum(xlims[0], np.min(timeE))
            ylims[0] = np.minimum(ylims[0], np.min(ipE / 1e6))
            xlims[1] = np.maximum(xlims[1], np.max(timeE))
            ylims[1] = np.maximum(ylims[1], np.max(ipE / 1e6))
        dy = ylims[1] - ylims[0]
        if dy > 0:
            ylims[0] = ylims[0] - 0.01 * dy
            ylims[1] = ylims[1] + 0.01 * dy
        elif ylims[0] != 0:
            ylims[0] = ylims[0] * 1.01
            ylims[1] = ylims[1] * 0.99
        else:
            xlims[0] = -1.0
            xlims[1] = +1.0
        dx = xlims[1] - xlims[0]
        if dx > 0:
            xlims[0] = xlims[0] - 0.01 * dx
            xlims[1] = xlims[1] + 0.01 * dx
        elif xlims[0] != 0:
            xlims[0] = xlims[0] * 1.01
            xlims[1] = xlims[1] * 0.99
        else:
            xlims[0] = -1.0
            xlims[1] = +1.0
        line33.set_xdata([time[time_index1]])
        ax.set_xlim(xlims)
        ax.set_ylim(ylims)

    def view_constraints(self, ax, time_index1, equilibrium2_ids=None):
        if self.equilibria is None:
            self.equilibria = self.compute_obj.get_equilibria()
            data = self.equilibria
        else:
            data = self.equilibria
        data2 = None
        if equilibrium2_ids:
            self.compute_obj2 = EquilibriumCompute(equilibrium2_ids)
            data2 = self.compute_obj2.get_equilibria()
            timeE = data["time"]
            constraintsE = data2["constraints"]
        time = data["time"]
        constraints = data["constraints"]

        (line41,) = ax.plot([], marker="x", color="darkgreen", label="target")
        (line42,) = ax.plot([], marker="x", color="darkblue", label="fitted")
        (line43,) = ax.plot([], marker="x", color="darkorange", label="target")
        (line44,) = ax.plot([], marker="x", color="maroon", label="fitted")
        ax.set_xlabel("index")

        if data2:
            result = self.compute_obj.get_constraints_info(
                "pf-currents", constraints, constraintsE, time, time_index1, timeE
            )
        else:
            result = self.compute_obj.get_constraints_info("pf-currents", constraints, None, time, time_index1, None)
        if result:
            y1in, y2in, y3in, y4in, titlelabel, ylabel, scaleFactor = result
            y1 = None
            y2 = None
            y3 = None
            y4 = None
            if y1in is not None:
                y1 = np.copy(y1in)
            if y2in is not None:
                y2 = np.copy(y2in)
            if y3in is not None:
                y3 = np.copy(y3in)
            if y4in is not None:
                y4 = np.copy(y4in)
            x_wrk = np.array([])
            y_wrk = np.array([])
            dataAvail = [False, False, False, False]
            dataAvail[0] = np.all(y1) is not None and np.any(y1 != imas.ids_defs.EMPTY_FLOAT)
            dataAvail[1] = np.all(y2) is not None and np.any(y2 != imas.ids_defs.EMPTY_FLOAT)
            dataAvail[2] = y3 is not None and np.any(y3 != imas.ids_defs.EMPTY_FLOAT)
            dataAvail[3] = y4 is not None and np.any(y4 != imas.ids_defs.EMPTY_FLOAT)
            if dataAvail[0]:
                x1 = range(len(y1))
                x_wrk = np.concatenate((x_wrk, x1))
                filtered = y1[y1 != imas.ids_defs.EMPTY_FLOAT]
                y1 /= scaleFactor
                if len(filtered) > 0:
                    y_wrk = np.concatenate((y_wrk, filtered / scaleFactor))
            if dataAvail[1]:
                x2 = range(len(y2))
                x_wrk = np.concatenate((x_wrk, x2))
                filtered = y2[y2 != imas.ids_defs.EMPTY_FLOAT]
                y2 /= scaleFactor
                if len(filtered) > 0:
                    y_wrk = np.concatenate((y_wrk, filtered / scaleFactor))
            if dataAvail[2]:
                x3 = range(len(y3))
                x_wrk = np.concatenate((x_wrk, x3))
                filtered = y3[y3 != imas.ids_defs.EMPTY_FLOAT]
                y3 /= scaleFactor
                if len(filtered) > 0:
                    y_wrk = np.concatenate((y_wrk, filtered / scaleFactor))
            if dataAvail[3]:
                x4 = range(len(y4))
                x_wrk = np.concatenate((x_wrk, x4))
                filtered = y4[y4 != imas.ids_defs.EMPTY_FLOAT]
                y4 /= scaleFactor
                if len(filtered) > 0:
                    y_wrk = np.concatenate((y_wrk, filtered / scaleFactor))

            minx = 0
            maxx = max(x_wrk)
            if maxx == 0:
                minx = -0.5
                maxx = +0.5
            else:
                dx = maxx - minx
                minx = minx - dx * 0.02
                maxx = maxx + dx * 0.02
            miny = min(y_wrk)
            maxy = max(y_wrk)
            dy = maxy - miny
            if dy == 0:
                dy = y_wrk[0]
            miny = miny - dy * 0.02
            maxy = maxy + dy * 0.02
            if dy == 0 and miny == 0:
                miny = -1
                maxy = +1

            if dataAvail[0]:
                line41.set_xdata(x1)
                line41.set_ydata(y1)
            else:
                line41.set_xdata(np.empty((0)))
                line41.set_ydata(np.empty((0)))
            if dataAvail[1]:
                line42.set_xdata(x2)
                line42.set_ydata(y2)
            else:
                line42.set_xdata(np.empty((0)))
                line42.set_ydata(np.empty((0)))
            if dataAvail[2]:
                line43.set_xdata(x3)
                line43.set_ydata(y3)
            else:
                line43.set_xdata(np.empty((0)))
                line43.set_ydata(np.empty((0)))
            if dataAvail[3]:
                line44.set_xdata(x4)
                line44.set_ydata(y4)
            else:
                line44.set_xdata(np.empty((0)))
                line44.set_ydata(np.empty((0)))
            if np.any(dataAvail):
                ax.set_ylabel(ylabel)
                ax.set_title(titlelabel)
                ax.set_xlim(minx, maxx)
                ax.set_ylim(miny, maxy)
