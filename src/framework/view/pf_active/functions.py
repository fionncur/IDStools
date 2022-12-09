# from ...common.BasePlot import font, ticksize

# TODO naming of the file
# fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
#     self.data["shot"], self.data["run"], self.data["time"]
# )

import matplotlib, os, sys

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# TODO Remove this class
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
        self.fig, self.axes_array = plt.subplots()

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


class PFCoilsPlot:
    def __init__(self, ax):
        self.ax = ax

    def overlay(self, coils_data):
        for coil_key, coil_data in coils_data.items():
            for element_key, element_data in coil_data:
                cec, cew, ceh = element_data
                rectangle = Rectangle(cec, cew, ceh)

                self.ax.add_patch(rectangle)
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width() / 2.0
                cy = ry + rectangle.get_height() / 2.0
                self.ax.annotate(
                    coil_key,
                    (cx, cy),
                    color="black",
                    weight="bold",
                    ha="center",
                    va="center",
                )
