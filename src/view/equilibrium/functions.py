from ...view.common.functions import BasePlot
from ...compute.equilibrium.functions import EquilibriumCompute


class EquilibriumView(BasePlot):
    def __init__(self, ax, ids_object):
        super().__init__(ax)
        self.ids_object = ids_object

    def magnetic_poloidal_flux(self):
        data = EquilibriumCompute.get_cartesian_rz_grid(self.ids_object)
        levels = 30

        if data["plotrho"]:
            self.ax.contour(
                data["r2d"], data["z2d"], data["rho2d"], data["levels"], colors="r"
            )
        self.ax.contour(data["r2d"], data["z2d"], data["psi2d"], levels)
        self.ax.set_xlim(data["r2d"].min(), data["r2d"].max())
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("$R$ [m]", fontdict=BasePlot.font)
        self.ax.set_ylabel("$Z$ [m]", fontdict=BasePlot.font)
        self.ax.tick_params(axis="both", which="major", labelsize=BasePlot.ticksize)
