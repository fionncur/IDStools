#!/usr/bin/env python3

import argparse
import imas
import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)


from idstools.view.common.basic import Canvas
from idstools.view.equilibrium.basic import EquilibriumView
from idstools.view.pf_active.basic import PFActiveView
from idstools.compute.common.basic import getClosestOfGivenValueFromArray
from idstools.utils.idslogger import setupLogger
from idstools.utils.clihelper import getBackendID, imasParser

parser = argparse.ArgumentParser(
    description="---- Display the plasma equilibrium from the equilibrium IDS. It also shows pf coils position overlay if exists",
    parents=[imasParser],
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
parser.add_argument(
    "--rho",
    help="Show pf coils overlay on the plot",
    action="store_true",
)
parser.add_argument(
    "--pfcoils",
    help="Show pf coils overlay on the plot",
    action="store_true",
)

parser.add_argument(
    "--save",
    help="Save figure at default location",
    action="store_true",
)
parser.add_argument(
    "-i",
    "--info",
    help="Adds all extra provenance info to the plot",
    action="store_true",
)
args = parser.parse_args()

logger = setupLogger("module")

database_abs_path = ""
database_abs_path = (
    (os.environ["IMAS_HOME"] + "/shared/imasdb/" + args.database + "/3")
    if args.user == "public"
    else f'{os.path.expanduser(f"~{args.user}")}/public/imasdb/{args.database}/3'
)
hostdir = os.environ["HOSTNAME"] + ":" + database_abs_path

connection = imas.DBEntry(
    getBackendID(args.backend), args.database, args.shot, args.run, args.user
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

idsObjEquilibrium = imas.equilibrium()
idsObjEquilibrium.time = connection.partial_get("equilibrium", "time", args.occurrence)
if idsObjEquilibrium.time is not None:
    timeIndex, timeValue = getClosestOfGivenValueFromArray(
        idsObjEquilibrium.time, args.time
    )
    idsObjEquilibrium.time_slice.resize(1)
    idsObjEquilibrium.time_slice[0] = connection.partial_get(
        "equilibrium", f"time_slice({str(timeIndex)})", args.occurrence
    )
    title = "2D Equilibrium"
    canvas = Canvas(1, 1)
    ax = canvas.add_axes(title="", xlabel="", row=0, col=0)

    if args.pfcoils is True:
        idsObjPfActive = imas.pf_active()
        idsObjPfActive.coil = connection.partial_get("pf_active", "coil")
        ViewPfCoils = PFActiveView(idsObjPfActive)
        ViewPfCoils.viewActivePfCoils(ax)
        title += " Active PF Coils"

    idsObjEquilibrium = connection.get("equilibrium")
    ViewEquilibrium = EquilibriumView(idsObjEquilibrium)
    ViewEquilibrium.viewMagneticPoloidalFlux(ax, plotRho=args.rho)

    if args.info is True:
        ViewEquilibrium.viewPulseInfo(ax, title, hostdir, args.shot, args.run, args.time)
    ax.set_title(title)
    ax.plot()

    if args.save:
        try:
            fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
                args.shot, args.run, args.time
            )
            canvas.save(fname)
            logger.info(f"----> Figure saved to {fname}")
        except Exception:
            logger.error("The figure could not be saved (check local permissions).")
    else:
        canvas.show()
else:
    logger.warning(
        "Can not produce plot, equilibrium/time is None"
    )