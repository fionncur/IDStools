""" 
This module provides view functions and classes for equilibrium ids data

`refer data dictionary <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/sphinx/latest.html>`

"""
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
from idstools.view.common import BasePlot
from idstools.compute.equilibrium import EquilibriumCompute


class EquilibriumView(BasePlot):
    def __init__(self, ids: object):
        """
        This is a constructor function that initializes an object with an input object and creates
        another object using the input object.

        Args:
            idsObj (object): The parameter `idsObj` is an object that is being passed to the constructor
        of the class. It is not clear from the code snippet what type of object it is, but it is being
        stored as an instance variable `self.idsObj`.
        """
        self.ids = ids
        self.computeObj = EquilibriumCompute(ids)

    def viewMagneticPoloidalFlux(
        self,
        ax: plt.Axes,
        timeSlice: int = 0,
        profiles2DIndex: int = 0,
        plotRho: bool = False,
    ):
        """
        This function plots the magnetic poloidal flux contours on a 2D Cartesian grid.

        Args:
            ax: `ax` is a matplotlib axis object on which the magnetic poloidal flux contour plot will be drawn.

        Example:
            .. code-block:: python

                import imas
                from idstools.view.equilibrium import EquilibriumView
                from idstools.view.common import Canvas

                input = imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,'ITER',134173,106,'public')
                input.open()
                idsObj = input.get('equilibrium')

                canvas = Canvas(1, 1) # create canvas
                ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

                viewObj = EquilibriumView(idsObj)
                viewObj.viewMagneticPoloidalFlux(ax) # plot contour on the canvas axes

                ax.plot()
                canvas.show()

            .. image:: ../../_static/images/EquilibriumView_viewMagneticPoloidalFlux.png
                :alt: image not found
                :align: center

        See also:
            :func:`idstools.compute.equilibrium.EquilibriumCompute.get2DCartesianGrid`
            :func:`idstools.compute.equilibrium.EquilibriumCompute.getRho2D`

            :meth:`plot_ip`
        """
        cartestionGrid = self.computeObj.get2DCartesianGrid(timeSlice, profiles2DIndex)
        if cartestionGrid is not None:
            levels = 30
            if plotRho:
                rho2d = self.computeObj.getRho2D()
                if rho2d is not None:
                    ax.contour(
                        cartestionGrid["r2d"],
                        cartestionGrid["z2d"],
                        rho2d,
                        levels,
                        colors="r",
                    )
            ax.contour(
                cartestionGrid["r2d"],
                cartestionGrid["z2d"],
                cartestionGrid["psi2d"],
                levels,
            )
            ax.set_aspect("equal", adjustable="box")
            ax.set_xlabel("$R$ [m]")
            ax.set_ylabel("$Z$ [m]")
            ax.tick_params(axis="both", which="major")

    def viewPulseInfo(
        self, ax: plt.axes, title: str, hostdir: str, shot: int, run: int, t: float
    ):
        self.database_info(ax, title, hostdir, shot, run, t)

    def plotIP(self, ax):
        """
        This function plots the plasma current over time on a given axis.

        Args:
            ax: The parameter "ax" is a matplotlib axis object.
        """
        plasmaCurrent = self.computeObj.getIP()
        time_array = self.ids.time

        ax.plot(time_array, plasmaCurrent, color="b", label="$I_p$ [MA]")

        ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(plasmaCurrent)*1.2)
        ax.set_ylim(0, 20)

    def plotPoloidalEquilibrium(self, ax, timeSlice: int):
        """
        This function plots a poloidal equilibrium contour plot using flux surface quantities extracted from the equilibrium.

        Args:
            ax: `ax` is a matplotlib axis object.
            timeSlice (int): timeSlice is an integer index.

        Returns:
            the contour plot object `cntr`.
        """
        # Extract flux surface quantities from equilibrium
        data = self.computeObj.getFluxSurfaces(timeSlice)
        r2d = data["r2d"]
        z2d = data["z2d"]
        rho2d = data["rho2d"]
        psi2d = data["psi2d"]
        cntr = ax.contour(r2d, z2d, psi2d, 50, cmap="summer")
        # if len(rho2d)>0:
        #    cntr = ax_polview.contour(r2d,z2d,rho2d,50,cmap='YlOrBr')

        # ax_polview.set_xlim(r2d.min(),r2d.max())
        ax.set_xlim(3.4, r2d.max())
        ax.set_ylim(z2d.min() * 0.7, z2d.max() * 0.7)
        ax.set_aspect("equal", adjustable="box")

        return cntr

    def plotTopviewEquilibrium(self, ax, timeIndex, label="Plasma Boundaries"):
        """
        This function plots the top view equilibrium of a plasma and updates the plot if specified.

        Args:
            ax: `ax` is a matplotlib axis object.
            timeIndex: The time index is an integer
            update: `update` is a boolean parameter that determines whether the plot should be updated or
        not. If `update` is `True`, the plot will be updated with new data. If `update` is `False`, the
        existing plot will be modified with new data. Defaults to True

        Returns:
            list containing two plot objects: ax_topview_plot_eq1 and ax_topview_plot_eq2.
        """
        # TODO: Refactor update mechanism of the plot
        data = self.computeObj.getTopView(timeIndex)
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
        ax.set_xlim(
            (-data["r0"] - data["amin"]) * 1.1, (data["r0"] + data["amin"]) * 1.1
        )
        ax.set_aspect("equal")

    def viewEquilibrium(self, ax):
        quantities = self.computeObj.get2DCartesianGrid()
        if quantities != None:
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

            ax.set_xlabel("$R\/\mathrm{[m]}$")
            # ax.tick_params(axis='both',which='major',labelsize=ticksize)
            ax.set_ylabel(r"$Z\/\mathrm{[m]}$")
            # ax.tick_params(
            #     axis="x", which="both", bottom=False, top=False, labelbottom=False
            # )
            ax.set_title("2D equilibrium")
        else:
            ax.text(0.2, 0.5, "2D equilibrium", fontsize=10)
            ax.text(0.2, 0.45, "not available", fontsize=10)

    def showInfoOnPlot(self, ax, info: str = "", location="right"):
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
