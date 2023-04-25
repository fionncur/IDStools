from ...view.common.functions import BasePlot
from ...compute.equilibrium.functions import EquilibriumCompute
import numpy as np


class EquilibriumView(BasePlot):
    def __init__(self, ids_object):
        self.equilibrium_object = ids_object
        self.equilibrium_compute_object = EquilibriumCompute(ids_object)

    def view_magnetic_poloidal_flux(self, ax):
        data = self.equilibrium_compute_object.get_cartesian_rz_grid()
        levels = 30

        if data["plotrho"]:
            ax.contour(
                data["r2d"], data["z2d"], data["rho2d"], data["levels"], colors="r"
            )
        ax.contour(data["r2d"], data["z2d"], data["psi2d"], levels)
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("$R$ [m]", fontdict=BasePlot.font)
        ax.set_ylabel("$Z$ [m]", fontdict=BasePlot.font)
        ax.tick_params(axis="both", which="major", labelsize=BasePlot.ticksize)

    def view_database_info(self, ax, title, hostdir, shot, run, t):
        self.database_info(ax, title, hostdir, shot, run, t)

    def plot_ip(self, ax):
        ip = self.equilibrium_compute_object.get_ip()
        time_array = self.equilibrium_object.time

        ax.plot(time_array, ip, color="b", label="$I_p$ [MA]")

        ax.set_xlim(min(time_array), max(time_array))
        # ax_waveform.set_ylim(0,max(ip)*1.2)
        ax.set_ylim(0, 20)

    def plot_poloidal_equilibrium(self, ax, time_index):
        # Extract flux surface quantities from equilibrium
        r2d, z2d, rho2d, psi2d = self.equilibrium_compute_object.get_flux_surfaces(
            time_index
        )

        cntr = ax.contour(r2d, z2d, psi2d, 50, cmap="summer")
        # if len(rho2d)>0:
        #    cntr = ax_polview.contour(r2d,z2d,rho2d,50,cmap='YlOrBr')

        # ax_polview.set_xlim(r2d.min(),r2d.max())
        ax.set_xlim(3.4, r2d.max())
        ax.set_ylim(z2d.min() * 0.7, z2d.max() * 0.7)
        ax.set_aspect("equal", adjustable="box")

        return cntr

    def plot_topview_equilibrium(self, ax, time_index, init=1):
        bndcolor = "chocolate"
        colorcounter = 0

        # Top view plot
        data = self.equilibrium_compute_object.get_top_view(time_index)

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
