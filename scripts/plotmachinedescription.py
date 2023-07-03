import argparse
import imas
import sys
import os

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from idstools.utils.clihelper import getBackendID
from idstools.utils.clihelper import imasParser
from idstools.set_logger import set_logger

from idstools.view.common.basic import Canvas
from idstools.view.pf_active.basic import PFActiveView
from idstools.view.wall.basic import WallView


# ----------------------------------------------------------------------

import yaml

logger = set_logger("mdplot", level="INFO")


def loadMD(d, s):

    for k, v in d.items():
        if k not in s:
            continue

        shot, run = k.split("/")
        db = imas.DBEntry(
            getBackendID(args.backend), args.database, int(shot), int(run), args.user
        )

        err, n = db.open()

        if err != 0:
            # TODO chek if you can raise exception or just print or may be use logger
            print(
                "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
                    shot, run, args.user, args.database
                ),
                file=sys.stderr,
            )
            print("----> Aborted.", file=sys.stderr)
            exit()

        d[k]["data"] = db.get(v["ids"])

    return d


def plotMD(d):

    # Initialization
    canvas = Canvas(1, 1)
    ax = canvas.add_axes(
        title="Machine Description", xlabel="R (m)", ylabel="Z (m)", row=0, col=0
    )

    # Custom settings
    canvas.fig.set_size_inches(7.5, 10.0)
    ax.set_aspect("equal", adjustable="box")

    # Plot Overlay
    # for k, v in d.items():

    pfcoilsview = PFActiveView(d["111001/102"]["data"])
    pfcoilsview.viewActivePfCoils(ax)

    wallview = WallView(d["116000/2"]["data"])
    wallview.view_wall(ax)

    # wallview.view_DIR(ax)
    # wallview.view_TS(ax)
    # wallview.view_Cryostat(ax)

    ax.plot()

    # try:
    #    fname = "Equilibrium_shot_{0}_run_{1}_time_{2:.1f}.png".format(
    #        args.shot, args.run, args.time
    #    )
    #    canvas.save(fname)
    #    print("----> Figure saved to " + fname, file=sys.stderr)
    # except:
    #    print("The figure could not be saved (check local permissions).", file=sys.stderr)

    canvas.show()


def main():

    logger.info("Start of MDPLOT")

    #
    logger.info("Reading meta data of MD")
    fpath = "/work/imas/shared/imasdb/ITER_MD/3/md_summary.yaml"
    with open(fpath, "r") as stream:
        try:
            mdin = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    #
    logger.info("Set target components")
    target = ["111001/102", "116000/2"]

    #
    logger.info("Loading MD database")
    data = loadMD(mdin, target)

    #
    logger.info("Plotting MD")
    plotMD(data)

    #
    logger.info("End of MDPLOT")


# ----------------------------------------------------------------------


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="---- Display the plasma equilibrium from the equilibrium IDS",
        parents=[imasParser],
    )
    args = parser.parse_args()
    main()
