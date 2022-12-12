# from ...common.BasePlot import font, ticksize

# TODO naming of the file
# fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
#     self.data["shot"], self.data["run"], self.data["time"]
# )

font = {
    "family": "serif",
    "color": "darkred",
    "weight": "normal",
    "size": 18,
}
ticksize = 15


class InformationDataInterface:
    def __init__(self) -> None:
        self.hostdir = None
        self.shot = None
        self.run = None
        self.is_show_info = False


class EquilibriumPlotDataInterface(InformationDataInterface):
    def __init__(self) -> None:
        self.r2d = None
        self.z2d = None
        self.rho2d = None
        self.psi2d = None
        self.time = None
        self.plotrho = None
        self.levels = None


class EquilibriumPlot:
    def __init__(self, ax):
        self.ax = ax

    def overlay(self, data):
        if data.plotrho:
            self.ax.contour(data.r2d, data.z2d, data.rho2d, data.levels, colors="r")
        self.ax.contour(data.r2d, data.z2d, data.psi2d, data.levels)
        self.ax.set_xlim(data.r2d.min(), data.r2d.max())
        self.ax.set_aspect("equal", adjustable="box")
        self.ax.set_xlabel("$R$ [m]", fontdict=font)
        self.ax.set_ylabel("$Z$ [m]", fontdict=font)
        # self.ax.set_xticks(ticks=ticksize)
        # self.ax.set_yticks(ticks=ticksize)

        if data.is_show_info:
            self.overlay_info(data)
        # from matplotlib.offsetbox import AnchoredText
        # anchored_text = AnchoredText('Shot '+str(shot)+' / '+'Run '+str(run),prop=dict(size=8),loc=4)
        # ax.add_artist(anchored_text)

    def overlay_info(self, data):
        plottitle = "2D equilibrium"
        plottitle += " (t={:.3f})".format(0)
        self.ax.set_title(plottitle, fontdict=font)

        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        self.ax.text(
            xmax + 0.01 * abs(xmax),
            ymin + 0.5 * abs(ymax - ymin),
            "{0}-Shot:{1},{2}".format(data.hostdir, data.shot, data.run),
            horizontalalignment="left",
            verticalalignment="center",
            rotation="vertical",
            fontsize=7,
        )
