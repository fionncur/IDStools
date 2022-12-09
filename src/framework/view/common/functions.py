import matplotlib, os, sys

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt


class BasePlot:
    # Tick size and X and Y axes
    ticksize = 15

    # Font definition
    font = {
        "family": "serif",
        "color": "darkred",
        "weight": "normal",
        "size": 18,
    }

    def __init__(self, nrows=1, ncols=1, width=4.5, height=6.5, dpi=100) -> None:
        self.width = width
        self.height = height
        self.dpi = dpi
        self.fig, self.axes = plt.subplots(nrows=nrows, ncols=ncols)

    def save(self, fname):
        fig = plt.gcf()
        fig.set_size_inches(self.width, self.height)
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
