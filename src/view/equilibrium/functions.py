from ...view.common.functions import BasePlot
from ...compute.equilibrium.functions import EquilibriumCompute


class EquilibriumView:
    def __init__(self, ids_object):
        self.equilibrium_object = EquilibriumCompute(ids_object)
        self.ids_object = ids_object

    def plot_ip(self, ax):
        ip = self.equilibrium_object.get_ip()
        time_array = self.ids_object.time

        ax.plot(time_array, ip, color="b", label="$I_p$ [MA]")

        ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(ip)*1.2)
        ax.set_ylim(0, 20)

    def plot_poloidal_equilibrium(self, ax, time_index):

        # Extract flux surface quantities from equilibrium
        r2d, z2d, rho2d, psi2d = self.equilibrium_object.get_flux_surfaces(time_index)

        cntr = ax.contour(r2d, z2d, psi2d, 50, cmap="summer")
        # if len(rho2d)>0:
        #    cntr = ax_polview.contour(r2d,z2d,rho2d,50,cmap='YlOrBr')

        # ax_polview.set_xlim(r2d.min(),r2d.max())
        ax.set_xlim(3.4, r2d.max())
        ax.set_ylim(z2d.min() * 0.7, z2d.max() * 0.7)
        ax.set_aspect("equal", adjustable="box")

        return cntr

    def plot_topview_equilibrium(self, ax, time_index, init=1):
        import numpy as np

        bndcolor = "chocolate"
        colorcounter = 0

        # Top view plot
        data = self.equilibrium_object.get_top_view(time_index)

        ax_topview_plot_eq1 = 0
        ax_topview_plot_eq2 = 0
        if init == 1:
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
        if init == 1:
            return [ax_topview_plot_eq1, ax_topview_plot_eq2]
