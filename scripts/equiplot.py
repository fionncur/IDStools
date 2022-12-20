import argparse
import imas


from idstools.cli import get_backend_id
from idstools.cli import imas_parser

import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from src.view.common.functions import Figure

from src.view.equilibrium.functions import EquilibriumView
from src.view.pf_active.functions import PFCoilsView

from src.compute.common.functions import nearest

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


# Get ids Object - equilibrium
equilibrium_ids = imas.equilibrium()
equilibrium_ids.time = connection.partial_get("equilibrium", "time", args.occurrence)
time_index, time_value = nearest(equilibrium_ids.time, args.time)
equilibrium_ids.time_slice.resize(1)
equilibrium_ids.time_slice[0] = connection.partial_get(
    "equilibrium", "time_slice(" + str(time_index) + ")", args.occurrence
)
# Get ids Object - pf active
pf_active_ids = connection_other.get("pf_active")


figure = Figure(1, 2)
axes1 = figure.axes_array[0]
axes2 = figure.axes_array[1]

pfcoils_plot = PFCoilsView(axes1, pf_active_ids)
pfcoils_plot.pf_coils()

equilibrium_plot = EquilibriumView(axes2, equilibrium_ids)
equilibrium_plot.magnetic_poloidal_flux()
equilibrium_plot.database_info("2D Equilibrium", hostdir, args.shot, args.run)

axes1.plot()
axes2.plot()

try:
    fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
        args.shot, args.run, args.time
    )
    figure.save(fname)
    print("----> Figure saved to " + fname, file=sys.stderr)
except:
    print("The figure could not be saved (check local permissions).", file=sys.stderr)

figure.show()
