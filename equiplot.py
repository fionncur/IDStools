import argparse
from src.framework.view.equilibrium.functions import BasePlot

from idstools.cli import imas_parser
from src.manager.equilibrium.plot_equilibrium import PlotEquilibrium

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

baseplot = BasePlot()
ax = baseplot.axes_array

plot_equilibrium = PlotEquilibrium(
    ax,
    args.database,
    args.backend,
    args.shot,
    args.run,
    args.user,
    args.occurrence,
    args.time,
    True,
)
plot_equilibrium.generate()
baseplot.show()
