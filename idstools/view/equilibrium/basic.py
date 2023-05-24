""" 
This module provides view functions and classes for equilibrium ids data

`more about equilibrium ids <https://sharepoint.iter.org/departments/POP/CM/IMDesign/Data%20Model/CI/imas-3.37.2/equilibrium.html>`_.

"""

import matplotlib.pyplot as plt
from ...view.common.basic import BasePlot
from ...compute.equilibrium.basic import EquilibriumCompute


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
                from idstools.view.equilibrium.basic import EquilibriumView
                from idstools.view.common.basic import Canvas

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
            :func:`idstools.compute.equilibrium.basic.EquilibriumCompute.get2DCartesianGrid`
            :func:`idstools.compute.equilibrium.basic.EquilibriumCompute.getRho2D`

            :meth:`plot_ip`
        """
        cartestionGrid = self.computeObj.get2DCartesianGrid(
            timeSlice, profiles2DIndex
        )
        if cartestionGrid is not None:
            levels = 30
            if plotRho:
                if rho := self.computeObj.getRho2D():
                    ax.contour(
                        cartestionGrid["r2d"],
                        cartestionGrid["z2d"],
                        cartestionGrid["rho2d"],
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
            ax.set_xlabel("$R$ [m]", fontdict=BasePlot.font)
            ax.set_ylabel("$Z$ [m]", fontdict=BasePlot.font)
            ax.tick_params(axis="both", which="major", labelsize=BasePlot.ticksize)

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

    def plotTopviewEquilibrium(self, ax, timeIndex, update=True):
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
        ax_topview_plot_eq1 = 0
        ax_topview_plot_eq2 = 0
        if update == True:
            bndcolor = "chocolate"
            colorcounter = 0

            if colorcounter == 1:
                (ax_topview_plot_eq1,) = ax.plot(
                    data["xpla"],
                    data["ypla"],
                    color=bndcolor,
                    label="Plasma Boundaries",
                )
            else:
                (ax_topview_plot_eq1,) = ax.plot(
                    data["xpla"], data["ypla"], color=bndcolor
                )
            (ax_topview_plot_eq2,) = ax.plot(
                data["xplap"], data["yplap"], color=bndcolor
            )
            ax.set_xlim(
                (-data["r0"] - data["amin"]) * 1.1, (data["r0"] + data["amin"]) * 1.1
            )
            ax.set_aspect("equal")
        else:
            ax[0].set_data(data["xpla"], data["ypla"])
            ax[1].set_data(data["xplap"], data["yplap"])
        if update == True:
            return [ax_topview_plot_eq1, ax_topview_plot_eq2]
