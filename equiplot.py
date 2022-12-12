import argparse

from idstools.cli import imas_parser
from src.manager.equilibrium.plot_equilibrium import PlotEquilibrium
from src.manager.pf_active.plot_pf_active import PlotPFActiveCoils

parser = argparse.ArgumentParser(
    description="---- Display the plasma equilibrium from the equilibrium IDS",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
parser.add_argument(
    "-t", "--time", help="Time (default=middle)", type=float, default=-99.0
)
parser.add_argument(
    "-o",
    "--occurrence",
    help="Occurrence number (default=%(default)s)",
    type=int,
    default=0,
)
parser.add_argument("-p", "--plotrho", help="Plots rho(R,Z)", action="store_true")
parser.add_argument(
    "-a",
    "--allInfo",
    help="Adds all extra provenance info to the plot",
    action="store_true",
)

args = parser.parse_args()


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
        self.fig, self.axes_array = plt.subplots(nrows, ncols)

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


baseplot = BasePlot(1, 2)
ax1 = baseplot.axes_array[0]
ax2 = baseplot.axes_array[1]

plot_equilibrium = PlotEquilibrium(
    ax2,
    args.database,
    args.backend,
    args.shot,
    args.run,
    args.user,
    args.occurrence,
    args.time,
    args.allInfo,
)

plot_pf_coils = PlotPFActiveCoils(
    ax1,
    "ITER_MD",
    args.backend,
    111001,
    202,
    args.user,
    args.occurrence,
)

plot_equilibrium.generate()
plot_pf_coils.generate()
ax1.plot()
ax1.plot()
baseplot.show()
