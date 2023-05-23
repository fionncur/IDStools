# Return values of an IDS in all data entries of a database

import sys
from imas import imasdef
import pandas as pd
import argparse
from pathlib import Path
from idstools.cli import *
from database_tools.db_helpers import *

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from idstools.database.basic import DatabaseTools

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extracts given quantities from all data entries of a given database",
        parents=[imas_parser],
    )
    parser.add_argument(
        "idspath",
        type=str,  # nargs="*", #multiple paths not yet implemented
        help="IDS path (starting with IDS name) to the desired data to be collected, e.g equilibrium/time",
    )
    parser.add_argument(
        "--saveas",
        type=str,
        help="File in which to store the results of this query, in csv format",
    )
    parser.add_argument(
        "--status",
        type=str,
        help="Will list only data entries with specified status (if such metadata is available)",
    )
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    locpath = getDBPath(args.user, args.database, args.version)
    # if args.verbose:
    #    print(f"database located in {locpath}")

    backend = get_backend_id(args.backend)

    if backend == imasdef.MDSPLUS_BACKEND:
        pulses = mdsListPulseRun(locpath, with_status=args.status)
    elif backend == imasdef.HDF5_BACKEND:
        pulses = hdf5ListPulseRun(locpath)
    else:
        print(f"Functionality not yet implemented for backend {args.backend}")
        sys.exit()

    # if args.verbose:
    #    print(pulses)

    df = DatabaseTools.getIdsDataFrameFromPulseDatabase(
        args.user, args.database, args.version, backend, args.idspath, pulses
    )

    if args.saveas:
        if not Path(args.saveas).parent.exists():
            raise FileNotFoundError(
                "The path provided does not exist or has no such database file or directory. Please check spelling."
            )
        df.to_csv(args.saveas, na_rep="None", index=True, header=True)
    else:
        print(df.to_markdown())
