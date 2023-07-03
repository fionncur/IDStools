#!/usr/bin/env python3
import argparse
import os
import sys

import imas

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from idstools.database.basic import DBMaster
from idstools.utils.clihelper import getBackendID, imasParser
from idstools.utils.idshelper import getAvailableIdsAndOccurrences

progbar = True
try:
    from rich.progress import track
except ModuleNotFoundError:
    progbar = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Checks if spciefied ids is exists in scenario database",
        parents=[imasParser],
    )
    parser.add_argument(
        "ids",
        type=str,
        default=None,
        help="Name of the IDS to check if it is available in scenario",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    parser.add_argument(
        "--status",
        type=str,
        help="Will list only data entries with specified status (if such metadata is available)",
    )
    args = parser.parse_args()
    backend = getBackendID(args.backend)
    dbmaster = DBMaster(args.user, args.database, args.version)
    if args.verbose:
        print(f"database located in {dbmaster.locpath}")
        
    pulses = None
    if backend == imas.imasdef.MDSPLUS_BACKEND:
        pulses = dbmaster.getMdsPlusPulses(status=args.status)
    elif backend == imas.imasdef.HDF5_BACKEND:
        pulses = dbmaster.getHdf5Pulses()
    else:
        print(f"Functionality not yet implemented for backend {args.backend}")
        sys.exit()

    if pulses is not None:
        for pulse in (
            track(pulses, description="Analyzing DB...") if progbar else pulses
        ):
            connection = imas.DBEntry(
                getBackendID(args.backend),
                args.database,
                pulse[0],
                pulse[1],
                args.user,
            )
            connection.open()
            ids_list = getAvailableIdsAndOccurrences(connection)
            if any(args.ids in ids for ids in ids_list):
                print((pulse[0], pulse[1]))
