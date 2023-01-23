from ...view.common.functions import BasePlot
from ...compute.equilibrium.functions import EquilibriumCompute


class EquilibriumView(BasePlot):
    def __init__(self, ax):
        super().__init__(ax)

    @staticmethod
    def view_magnetic_poloidal_flux(ax, ids_object):
        data = EquilibriumCompute.get_cartesian_rz_grid(ids_object)
        equillibrium_view = EquilibriumView(ax)
        equillibrium_view.__magnetic_poloidal_flux(data)

    def view_database_info(ax, title, hostdir, shot, run, t):
        equillibrium_view = EquilibriumView(ax)
        equillibrium_view.database_info(title, hostdir, shot, run, t)

    def __magnetic_poloidal_flux(self, data):

        levels = 30

        if data["plotrho"]:
            self.ax.contour(
                data["r2d"], data["z2d"], data["rho2d"], data["levels"], colors="r"
            )
        self.ax.contour(data["r2d"], data["z2d"], data["psi2d"], levels)
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("$R$ [m]", fontdict=BasePlot.font)
        self.ax.set_ylabel("$Z$ [m]", fontdict=BasePlot.font)
        self.ax.tick_params(axis="both", which="major", labelsize=BasePlot.ticksize)
