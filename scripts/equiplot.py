import argparse
import imas


from idstools.cli import get_backend_id
from idstools.cli import imas_parser

import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from src.framework.view.common.functions import CommonPlot
from src.framework.view.common.functions import BasePlot

from src.framework.view.equilibrium.functions import EquilibriumPlot
from src.framework.view.pf_active.functions import PFCoilsPlot
from src.framework.compute.common.functions import compute_time_index

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


database_abs_path = ""
if args.user == "public":
    database_abs_path = (
        os.environ["IMAS_HOME"] + "/shared/imasdb/" + args.database + "/3"
    )
else:
    database_abs_path = (
        os.path.expanduser("~{}".format(args.user))
        + "/public/imasdb/"
        + args.database
        + "/3"
    )
hostdir = os.environ["HOSTNAME"] + ":" + database_abs_path

connection = imas.DBEntry(
    get_backend_id(args.backend), args.database, args.shot, args.run, args.user
)
err, n = connection.open()
if err != 0:
    # TODO chek if you can raise exception or just print or may be use logger
    print(
        "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
            args.shot, args.run, args.user, args.database
        ),
        file=sys.stderr,
    )
    print("----> Aborted.", file=sys.stderr)
    exit()

connection_other = imas.DBEntry(
    get_backend_id(args.backend), "ITER_MD", 111001, 202, args.user
)
err, n = connection_other.open()
if err != 0:
    # TODO chek if you can raise exception or just print or may be use logger
    print(
        "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
            args.shot, args.run, args.user, args.database
        ),
        file=sys.stderr,
    )
    print("----> Aborted.", file=sys.stderr)
    exit()


# Prepare IDS Object - equilibrium
equilibrium_object = eval("imas.equilibrium()")
equilibrium_object.time = connection.partial_get("equilibrium", "time", args.occurrence)
time_index, time_value = compute_time_index(equilibrium_object.time, args.time)
equilibrium_object.time_slice.resize(1)
equilibrium_object.time_slice[0] = connection.partial_get(
    "equilibrium", "time_slice(" + str(time_index) + ")", args.occurrence
)
# Prepare IDS Object - pf active
pf_active_object = connection_other.get("pf_active")


baseplot = BasePlot(1, 2)
ax1 = baseplot.axes_array[0]
ax2 = baseplot.axes_array[1]

equilibrium_plot_ax2 = EquilibriumPlot(ax2, equilibrium_object)
equilibrium_plot_ax2.overlay()

common_plot_ax2 = CommonPlot(ax2)
common_plot_ax2.overlay_info("2D Equilibrium", hostdir, args.shot, args.run)

pfcoils_plot_ax1 = PFCoilsPlot(ax1, pf_active_object)
pfcoils_plot_ax1.overlay()
ax1.plot()
ax2.plot()


try:
    fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
        args.shot, args.run, args.time
    )
    baseplot.save(fname)
    print("----> Figure saved to " + fname, file=sys.stderr)
except:
    print("The figure could not be saved (check local permissions).", file=sys.stderr)

baseplot.show()
