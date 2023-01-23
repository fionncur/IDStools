import matplotlib, os, sys

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt


class Figure:
    # Tick size and X and Y axes
    ticksize = 15

    # Font definition
    font = {
        "family": "serif",
        "color": "darkred",
        "weight": "normal",
        "size": 18,
    }

    def __init__(self, nrows=1, ncols=1) -> None:
        self.fig, self.axes_array = plt.subplots(nrows, ncols)

    def save(
        self,
        fname,
        width=4.5,
        height=6.5,
        dpi=100,
    ):
        fig = plt.gcf()
        fig.set_size_inches(width, height)
        try:
            fig.savefig(fname, dpi=self.dpi)
            print("----> Figure saved to " + fname, file=sys.stderr)
        except:
            print(
                "The figure could not be saved (check local permissions).",
                file=sys.stderr,
            )

    def show(self):
        plt.show()


class BasePlot:
    font = {
        "family": "serif",
        "color": "darkred",
        "weight": "normal",
        "size": 12,
    }
    ticksize = 10

    def __init__(self, ax):
        self.ax = ax

    def database_info(self, title, hostdir, shot, run, t):
        plottitle = title
        plottitle += " (t={:.3f})".format(t)
        self.ax.set_title(plottitle, fontdict=BasePlot.font)

        xmin, xmax = self.ax.get_xlim()
        ymin, ymax = self.ax.get_ylim()
        self.ax.text(
            xmax + 0.01 * abs(xmax),
            ymin + 0.5 * abs(ymax - ymin),
            "{0}-Shot:{1},{2}".format(hostdir, shot, run),
            horizontalalignment="left",
            verticalalignment="center",
            rotation="vertical",
            fontsize=7,
        )
        # from matplotlib.offsetbox import AnchoredText

        # anchored_text = AnchoredText(
        #     "Shot " + str(shot) + " / " + "Run " + str(run), prop=dict(size=8), loc=4
        # )
        # self.ax.add_artist(anchored_text)


class Console:
    tabsize = 10
    TAB = " " * 16
    LINE = "-" * 8

    def __init__(self) -> None:
        pass
