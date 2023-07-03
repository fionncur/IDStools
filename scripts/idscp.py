#!/usr/bin/env python

import argparse
import logging
import os
import sys

import imas



root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from idstools.utils.clihelper import getBackendID, imasParser
from idstools.utils.idslogger import setupLogger

logger = setupLogger("module")
# Management of input arguments
parser = argparse.ArgumentParser(
    description="Copy IDSs from a data-entry into another one",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[imasParser],
)

parser.add_argument(
    "-si", "--shot_input", help="Input shot number", required=True, type=int
)
parser.add_argument(
    "-ri", "--run_input", help="Input run number", required=True, type=int
)
parser.add_argument(
    "-so", "--shot_output", help="Output shot number", required=True, type=int
)
parser.add_argument(
    "-ro", "--run_output", help="Output run number", required=True, type=int
)
# default user from parent parser is 'public', which is fine for exploration scripts but less for management scripts
parser.set_defaults(user=os.environ["USER"])
parser.add_argument(
    "-do",
    "--database_output",
    type=str,
    default=None,
    help="Database name for the destination data-entry",
)
parser.add_argument(
    "-bo",
    "--backend_output",
    type=str,
    help="Backend name for the destination data-entry",
)
parser.add_argument(
    "-f",
    "--force",
    action="store_true",
    help="Force the creation of destination data-entry (existing data will be lost)",
)
parser.add_argument(
    "--setDatasetVersion",
    action="store_true",
    help="Store current DD version into dataset_description IDS if it exists",
)
occgroup = parser.add_mutually_exclusive_group()
occgroup.add_argument(
    "-a",
    "--allOccurrences",
    action="store_true",
    help="Copy all occurrences available in the source into the destination",
)
occgroup.add_argument(
    "-o",
    "--outputOccurrence",
    type=int,
    default=None,
    help="Copy the selected source into the specified occurrence at the destination",
)
parser.add_argument(
    "ids",
    nargs="*",
    type=str,
    help='IDSs to copy (leave empty to select all IDSs with default occurrence, or append "/n" to copy a specific occurrence "n")',
)
args = parser.parse_args()


if args.database_output is None:
    args.database_output = args.database


if args.backend_output is None:
    args.backend_output = args.backend

if (
    args.shot_input == args.shot_output
    and args.run_input == args.run_output
    and args.user == os.environ["USER"]
    and args.database == args.database_output
    and args.backend == args.backend_output
):
    logger.error("Can not use the same data-entry as source and destination!")
    exit()

if args.ids == []:
    args.ids = [ids.value for ids in list(imas.IDSName)]


# OPEN SOURCE
src_connection = imas.DBEntry(
    getBackendID(args.backend),
    args.database,
    args.shot_input,
    args.run_input,
    user_name=args.user,
)
status, _ = src_connection.open()
if status != 0:
    logger.error("Error opening source pulse! Please check existence.")
    sys.exit(status)


dest_connection = imas.DBEntry(
    getBackendID(args.backend_output),
    args.database_output,
    args.shot_output,
    args.run_output,
    user_name=os.environ["USER"],
)
if not args.force:
    # OPEN DEST
    status, _ = dest_connection.open()
    if status != 0:
        logger.warning("Destination pulse does not exist. Creating.")
        status, _ = dest_connection.create()
    if status != 0:
        logger.error("Error opening destination pulse! Please check parameters.")
        exit(status)
else:
    # CREATE DEST
    status, _ = dest_connection.create()
    if status != 0:
        logger.error(
            "Error creating destination pulse! Please check parameters and permissions."
        )
        exit(status)


if args.allOccurrences:
    if "/" in args.ids:
        logger.error(
            "Please do not specify source occurrences together with -a/--allOccurrences option"
        )
        exit(status)
    else:
        allids = []
        for idsname in args.ids:
            mocc = getattr(imas, idsname)().getMaxOccurrences()
            allids.append(idsname)
            allids.extend(f"{idsname}/{o}" for o in range(1, mocc + 1))
        args.ids = allids


# COPY IDSs FROM SOURCE TO DEST
for idsname in args.ids:
    inocc = 0
    idsid = idsname.split("/")
    if len(idsid) == 2:
        inocc = int(idsid[1])

    idsobj = src_connection.get(idsid[0], occurrence=inocc)
    if args.setDatasetVersion and idsid[0] == "dataset_description":
        idsobj.dd_version = os.environ["IMAS_VERSION"]
    try:
        if idsobj.ids_properties.homogeneous_time != imas.imasdef.EMPTY_INT:
            print(f"Copying {idsname}")
            outocc = inocc if args.outputOccurrence is None else args.outputOccurrence
            dest_connection.put(idsobj, occurrence=outocc)
    except Exception as exc:
        print(exc, file=sys.stderr)
        if not args.force:
            logger.warning(
                "This error could be due to difference of data dictionary version between the current one and the existing destination pulse"
            )
            logger.warning(
                "You can use option -f/--force to recreate the destination pulse with the current DD version (WARNING: all other IDSs will be lost at dest)"
            )

src_connection.close()
dest_connection.close()
