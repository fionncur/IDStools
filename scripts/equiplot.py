import argparse
import imas
import logging
import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from cli_helper import get_backend_id, imas_parser, setup_logger

from idstools2.view.common.basic import Canvas
from idstools2.view.equilibrium.basic import EquilibriumView
from idstools2.view.pf_active.basic import PFCoilsView
from idstools2.compute.common.basic import nearest


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
parser.add_argument(
    "-c",
    "--pfcoils",
    help="Show pf coils overlay on the plot",
    action="store_true",
)
args = parser.parse_args()


level = logging.WARN
logger = setup_logger("module", level)

database_abs_path = ""
database_abs_path = (
    (os.environ["IMAS_HOME"] + "/shared/imasdb/" + args.database + "/3")
    if args.user == "public"
    else f'{os.path.expanduser(f"~{args.user}")}/public/imasdb/{args.database}/3'
)
hostdir = os.environ["HOSTNAME"] + ":" + database_abs_path

connection = imas.DBEntry(
    get_backend_id(args.backend), args.database, args.shot, args.run, args.user
)
err, n = connection.open()
if err != 0:
    logger.error(
        "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
            args.shot, args.run, args.user, args.database
        )
    )
    raise FileNotFoundError(
        "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
            args.shot, args.run, args.user, args.database
        )
    )

# Get ids Object - equilibrium
equilibrium_ids = imas.equilibrium()
equilibrium_ids.time = connection.partial_get("equilibrium", "time", args.occurrence)
time_index, time_value = nearest(equilibrium_ids.time, args.time)
equilibrium_ids.time_slice.resize(1)
equilibrium_ids.time_slice[0] = connection.partial_get(
    "equilibrium", f"time_slice({str(time_index)})", args.occurrence
)
# Get ids Object - pf active
pf_active_ids = connection.get("pf_active")

canvas = Canvas(1, 1)
ax = canvas.add_axes(title="PF Coils", xlabel="", row=0, col=0)
# if args.pfcoils is True:
pfcoilsview = PFCoilsView(pf_active_ids)
pfcoilsview.view_pf_coils(ax)

equilibriumview = EquilibriumView(equilibrium_ids)

equilibriumview.view_magnetic_poloidal_flux(ax)
if args.allInfo is True:
    equilibriumview.view_database_info(
        ax, "2D Equilibrium", hostdir, args.shot, args.run, args.time
    )

ax.plot()

try:
    fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
        args.shot, args.run, args.time
    )
    canvas.save(fname)
    print(f"----> Figure saved to {fname}", file=sys.stderr)
except Exception:
    print("The figure could not be saved (check local permissions).", file=sys.stderr)

canvas.show()
