#!/usr/bin/env python

# @author: H.-J. Klingshirn
from __future__ import print_function
import optparse
import os
import sys
import numpy

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

import idstools.db_tools as dbtools


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


def print_times(dbs, opts, printTimes=False, shotnum=None, runnum=None):
    import idstools.ids_tools as ct

    for dbname, dvs in dbs:
        printed_database = False
        for dv, dbbackends in dvs:
            printed_dataversion = False
            for backend, dbs in dbbackends:
                printed_backend = False
                for shot, runs in dbs:
                    # If a shotnum and/or runnum is given, only display these
                    if shotnum is not None:
                        if shot != shotnum:
                            continue

                    printed_shot = False
                    justruns = [r[0] for r in runs]
                    for run in justruns:
                        if runnum is not None:
                            if run != runnum:
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
                            shot, run, opts.user, dbname, dv, True, backend == "hdf5"
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


p = optparse.OptionParser(
    usage="%prog [OPTIONS] [COMMAND]\n\
\n\
This program lists existing IMAS databases.\n\
\n\
Possible commands are: \n\
\tlist <shot number>- list existing databases \n\
\tslices <shot number> <run number> - list existing databases, including number of timeslices and time range for time-dependent IDSs\n\
\ttimes <shot number> <run number> - list existing databases, including number of timeslices their time points for time-dependent IDSs \n\
\tdatabases - list existing databases (with data versions)\n\
\tdataversions - list existing dataversions (with databases)\n\
\n\
If the optional arguments shot number and run number are given, only databases with these numbers will be shown.\n\
\n\
If no command is given, the list command is performed. \n\
\n\
To see databases stored in the public imas database, use 'public' as the user name.\
"
)
p.add_option(
    "-u", "--user", dest="user", default=None, help="Show databases of specified user"
)
p.add_option(
    "-t",
    "--tokamak",
    dest="dbname",
    default=None,
    help="[DEPRECATED, use -d instead] Show only databases with specified tokamak",
)
p.add_option(
    "-d",
    "--database",
    dest="dbname",
    default=None,
    help="Show only databases with specified name",
)
p.add_option(
    "-v",
    "--version",
    dest="version",
    default=None,
    help="Show only databases for specified major data version",
)
p.add_option(
    "--backend",
    dest="backend",
    default=None,
    help="Show databases written with given backend(s). \n\
Comma-separated list of backends (Currently supported: mdsplus, hdf5). By default all backends are shown.",
)
p.add_option(
    "-c",
    "--compact",
    action="store_true",
    dest="compact",
    default=False,
    help="Compact/reduced output",
)
p.add_option(
    "-M",
    "--lastModifiedDate",
    action="store_true",
    dest="timestamp",
    default=False,
    help="Show (and sort per) date of last modification of the runs",
)


opts, args = p.parse_args()

if not args or args[0] == "list" or args[0] == "slices" or args[0] == "times":
    # Default action: show databases
    shotnum = None
    if len(args) > 1:
        try:
            shotnum = int(args[1])
        except Exception:
            print("Second argument must be an integer", file=sys.stderr)
            sys.exit(1)

    runnum = None
    if len(args) > 2:
        try:
            runnum = int(args[2])
        except Exception:
            print("Third argument must be an integer", file=sys.stderr)
            sys.exit(1)

    if len(args) > 0 and args[0] in ["slices", "times"]:
        envdv = (os.getenv("IMAS_VERSION")).split(".")[0]

        if opts.version != None and envdv != opts.version:
            print(
                "Cannot access IDS times for data version differing from current major version "
                + envdv,
                file=sys.stderr,
            )
            sys.exit(1)

    backends = opts.backend.split(",") if opts.backend else None
    dbs = dbtools.list_databases(opts.user, opts.dbname, opts.version, backends)

    if args and args[0] == "slices":
        print_times(dbs, opts, printTimes=False, shotnum=shotnum, runnum=runnum)
    elif args and args[0] == "times":
        print_times(dbs, opts, printTimes=True, shotnum=shotnum, runnum=runnum)
    else:
        print_list(dbs, shotnum, opts.compact, opts.timestamp)

elif args[0] == "tokamaks":
    print(
        'Warning: "tokamaks" command is being deprecated and should be replaced by "databases"'
    )
    for dbname, dvs in dbtools.list_tokamaks(opts.user, opts.version):
        print(
            extended(dbname, DATABASE_STR_LEN)
            + " "
            + print_vector(dvs, VERSION_STR_LEN)
        )

elif args[0] == "databases":
    for dbname, dvs in dbtools.list_tokamaks(opts.user, opts.version):
        print(
            extended(dbname, DATABASE_STR_LEN)
            + " "
            + print_vector(dvs, VERSION_STR_LEN)
        )

elif args[0] == "dataversions":
    for dv, dbname in dbtools.list_dataversions(opts.user):
        print(
            extended(dv, VERSION_STR_LEN) + " " + print_vector(dbname, DATABASE_STR_LEN)
        )

else:
    print(
        "Unknown command: "
        + args[0]
        + ". Possible commands are (none), list, slices, times, databases, dataversions",
        file=sys.stderr,
    )
