#!/usr/bin/env python

import argparse
import os
import sys
import numpy
import textwrap


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from idstools.utils.dbhelper import getDatabaseFiles, getDatabases2, getDatabases
from idstools.cli import imas_parser
# import idstools.ids_tools as ct

TAB = " " * 3
SHOT_STR_LEN = 6
RUN_STR_LEN = 5
DATABASE_STR_LEN = 12
VERSION_STR_LEN = 6
IDSNAME_STR_LEN = 26
SLICENUM_STR_LEN = 4
RUNNUM_STR_LEN = 4
TIME_STR_LEN = 4


def extended(str, wlen):
    return f"{str:>{wlen}s}"


def print_vector(vec, wlen):
    return " ".join([f"{str(x):>{wlen}s}" for x in vec])


def print_list(dbs, shotnum=None, compact=False, timestamp=False):
    for dbname, dvs in dbs:
        printed_database = False
        for dv, dbbackends in dvs:
            printed_dataversion = False
            for backend, dbs in dbbackends:
                printed_backend = False
                for shot, runs in dbs:
                    if shotnum is not None:
                        # if a shotnum is given, only display databases with this shot number
                        if shot != shotnum:
                            continue

                    if not printed_database:
                        print(f"Database: {dbname}")
                        printed_database = True
                    if not printed_dataversion:
                        print(f"{TAB}Data version: {dv}")
                        printed_dataversion = True
                    if not printed_backend:
                        print(TAB * 2 + "UAL Backend: " + backend)
                        printed_backend = True
                    if compact:
                        print(
                            TAB * 3
                            + "Shot "
                            + extended(str(shot), SHOT_STR_LEN)
                            + ": "
                            + extended(str(len(runs)), RUNNUM_STR_LEN)
                            + " runs"
                        )

                    elif timestamp:
                        print(TAB * 3 + "Shot " + extended(str(shot), SHOT_STR_LEN))
                        runs.sort(reverse=True, key=lambda x: x[1])
                        for r in runs:
                            print(
                                TAB * 3
                                + " " * (5 + SHOT_STR_LEN)
                                + " Runs: "
                                + extended(str(r[0]), RUN_STR_LEN)
                                + " ("
                                + str(r[1])
                                + ")"
                            )
                    else:
                        print(
                            TAB * 3
                            + "Shot "
                            + extended(str(shot), SHOT_STR_LEN)
                            + " Runs: "
                            + print_vector([r[0] for r in runs], RUN_STR_LEN)
                        )


def print_times(dbs, arguements, printTimes=False, shot=None, run=None):
    for dbname, dvs in dbs:
        printed_database = False
        for dv, dbbackends in dvs:
            printed_dataversion = False
            for backend, dbs in dbbackends:
                printed_backend = False
                for shot, runs in dbs:
                    # If a shotnum and/or runnum is given, only display these
                    if shot is not None:
                        if shot != shot:
                            continue

                    printed_shot = False
                    justruns = [r[0] for r in runs]
                    for run in justruns:
                        if run is not None:
                            if run != run:
                                continue

                        if not printed_database:
                            print(f"Tokamak: {dbname}")
                            printed_database = True
                        if not printed_dataversion:
                            print(f"{TAB}Data version: {dv}")
                            printed_dataversion = True
                        if not printed_backend:
                            print(TAB * 2 + "UAL Backend: " + backend)
                            printed_backend = True
                        if not printed_shot:
                            print(TAB * 3 + "Shot " + extended(str(shot), SHOT_STR_LEN))
                            printed_shot = True

                        print(TAB * 4 + " Run: " + extended(str(run), RUN_STR_LEN))
                        db = ct.ImasDb(
                            shot,
                            run,
                            arguements.user,
                            dbname,
                            dv,
                            True,
                            backend == "hdf5",
                        )
                        alltimes = db.all_times()
                        for idsname, times in alltimes:
                            if len(times) == 1 and numpy.isnan(times[0]):
                                print(
                                    TAB * 5
                                    + extended(idsname, IDSNAME_STR_LEN)
                                    + ": "
                                    + extended("?", SLICENUM_STR_LEN)
                                    + " slices ( "
                                    + "heterogeneous IDS )"
                                )
                            elif len(times) == 1 and times[0] == numpy.NINF:
                                print(
                                    TAB * 5
                                    + extended(idsname, IDSNAME_STR_LEN)
                                    + ": "
                                    + extended("?", SLICENUM_STR_LEN)
                                    + " slices ( "
                                    + "time independent IDS )"
                                )
                            elif printTimes:
                                print(
                                    TAB * 5
                                    + extended(idsname, IDSNAME_STR_LEN)
                                    + ": "
                                    + extended(str(len(times)), SLICENUM_STR_LEN)
                                    + " slices ("
                                    + print_vector(times, TIME_STR_LEN)
                                    + ")"
                                )
                            else:
                                print(
                                    TAB * 5
                                    + extended(idsname, IDSNAME_STR_LEN)
                                    + ": "
                                    + extended(str(len(times)), SLICENUM_STR_LEN)
                                    + " slices ("
                                    + extended(str(times[0]), TIME_STR_LEN)
                                    + " - "
                                    + extended(str(times[-1]), TIME_STR_LEN)
                                    + ")"
                                )

                        db.close()


# argparse.ArgumentParser
parser = argparse.ArgumentParser(
    prog="imasdbs",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=textwrap.dedent(
        """            
            This program lists existing IMAS databases.

            Possible commands are: 
            list <shot number>- list existing databases 
            slices <shot number> <run number> - list existing databases, including number of timeslices and time range for time-dependent IDSs
            times <shot number> <run number> - list existing databases, including number of timeslices their time points for time-dependent IDSs 
            databases - list existing databases (with data versions)
            dataversions - list existing dataversions (with databases)

            If the optional arguments shot number and run number are given, only databases with these numbers will be shown.

            If no command is given, the list command is performed. 

            To see databases stored in the public imas database, use 'public' as the user name."""
    ),
)
subparsers = parser.add_subparsers(help="sub-commands help")

subparserList = subparsers.add_parser("list", help="list databases")
subparserList.set_defaults(cmd="list")

subparserList.add_argument(
    "-c",
    "--compact",
    action="store_true",
    dest="compact",
    default=False,
    help="Compact/reduced output",
)
subparserList.add_argument(
    "-M",
    "--lastModifiedDate",
    action="store_true",
    dest="timestamp",
    default=False,
    help="Show (and sort per) date of last modification of the runs",
)
subparserList.add_argument("shot", nargs="?", help="Shot number", type=int)

subparserSlices = subparsers.add_parser("slices", help="list slices")
subparserSlices.set_defaults(cmd="slices")
subparserSlices.add_argument("shot", nargs="?", help="Shot number", type=int)
subparserSlices.add_argument("run", nargs="?", help="Run number", type=int)
subparserTimes = subparsers.add_parser("times", help="list times")
subparserTimes.set_defaults(cmd="times")
subparserTimes.add_argument("shot", nargs="?", help="Shot number", type=int)
subparserTimes.add_argument("run", nargs="?", help="Run number", type=int)

subparserDatabases = subparsers.add_parser("databases", help="print databases")
subparserDatabases.set_defaults(cmd="databases")

subparserDataVersions = subparsers.add_parser(
    "dataversions", help="print data versions"
)
subparserDataVersions.set_defaults(cmd="dataversions")

parser.add_argument(
    "-u",
    "--user",
    dest="user",
    default=None,
    help="Show databases of specified user \t\t(default=%(default)s)",
)
parser.add_argument(
    "-d",
    "--database",
    dest="database",
    default=None,
    help="Show only databases with specified name \t(default=%(default)s)",
)
parser.add_argument(
    "-v",
    "--version",
    dest="version",
    default=None,
    help="Show only databases for specified major data version \t(default=%(default)s)",
)
parser.add_argument(
    "--backend",
    dest="backend",
    default=None,
    help="Show databases written with given backend(s). \n\
Comma-separated list of backends (Currently supported: mdsplus, hdf5). By default all backends are shown. \t(default=%(default)s)",
)


parser.add_argument("positionalArgs", nargs="?", default=os.getcwd())

args = parser.parse_args()

try:
    if args.cmd is None:
        parser.print_help()
        exit(1)
except AttributeError:
    parser.print_help()
    exit(1)

backends = args.backend.split(",") if args.backend else None
dbs = getDatabaseFiles(args.user, args.database, args.version, backends)
if args.cmd == "list":
    print_list(dbs, args.shot, args.compact, args.timestamp)
if args.cmd == "slices":
    print_times(dbs, args, printTimes=False, shot=args.shot, run=args.run)

if args.cmd == "times":
    print_times(dbs, args, printTimes=True, shot=args.shot, run=args.run)

if args.cmd == "databases":
    for dbname, dvs in getDatabases(args.user, args.version):
        print(
            extended(dbname, DATABASE_STR_LEN)
            + " "
            + print_vector(dvs, VERSION_STR_LEN)
        )

if args.cmd == "dataversions":
    for dv, dbname in getDatabases2(args.user):
        print(
            f"{extended(dv, VERSION_STR_LEN)} {print_vector(dbname, DATABASE_STR_LEN)}"
        )
