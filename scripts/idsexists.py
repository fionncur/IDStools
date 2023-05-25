#!/usr/bin/env python3
import argparse
import os
import sys

import imas

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from database_tools import db_helpers
from idstools import idslist
from idstools.cli import get_backend_id, imas_parser

progbar = True
try:
    from rich.progress import track
except ModuleNotFoundError:
    progbar = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Checks if spciefied ids is exists in scenario database",
        parents=[imas_parser],
    )
    parser.add_argument(
        "ids",
        type=str,
        default=None,
        help="Name of the IDS to check if it is available in scenario",
    )
    args = parser.parse_args()
    pulselist = None
    if get_backend_id(args.backend) == imas.imasdef.MDSPLUS_BACKEND:
        pulselist = db_helpers.mdsListPulseRun(
            "/work/imas/shared/imasdb/ITER/3/0", with_status="active"
        )
    elif get_backend_id(args.backend) == imas.imasdef.HDF5_BACKEND:
        pulselist = db_helpers.hdf5ListPulseRun(
            "/work/imas/shared/imasdb/ITER/3/0", with_status="active"
        )

    if pulselist is not None:
        for pulse in (
            track(pulselist, description="Analyzing DB...") if progbar else pulselist
        ):
            db = imas.DBEntry(
                get_backend_id(args.backend),
                args.database,
                pulse[0],
                pulse[1],
                args.user,
            )
            db.open()
            ids_list = idslist.available_in_dbentry(db)
            if any(args.ids in ids for ids in ids_list):
                print(pulse)
