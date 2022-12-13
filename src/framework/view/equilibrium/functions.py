from ...compute.equilibrium.functions import EquilibriumCompute


class EquilibriumPlot:
    font = {
        "family": "serif",
        "color": "darkred",
        "weight": "normal",
        "size": 18,
    }
    ticksize = 15

    def __init__(self, ax, ids_object):
        self.equilibrium_compute = EquilibriumCompute(ids_object)
        self.ax = ax

    def overlay(self):
        levels = 30

        data = self.equilibrium_compute.get_cartesian_r_z_grids()
        if data["plotrho"]:
            self.ax.contour(
                data["r2d"], data["z2d"], data["rho2d"], data["levels"], colors="r"
            )
        self.ax.contour(data["r2d"], data["z2d"], data["psi2d"], levels)
        self.ax.set_xlim(data["r2d"].min(), data["r2d"].max())
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("$R$ [m]", fontdict=EquilibriumPlot.font)
        self.ax.set_ylabel("$Z$ [m]", fontdict=EquilibriumPlot.font)
        self.ax.tick_params(
            axis="both", which="major", labelsize=EquilibriumPlot.ticksize
        )
