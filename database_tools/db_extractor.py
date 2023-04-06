#!/usr/bin/env python
# Return values of an IDS in all data entries of a database

import imas
import os,sys
from imas import imasdef
import pandas as pd
import argparse
from pathlib import Path
from idstools.cli import *
from database_tools.db_helpers import *
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False





def extract_from_db(dbuser, database, version, backend, idspath, pulses):
    """ Function that returns a pandas dataframe displaying all values of given IDSs extracted by the function.

    Parameters
    ---------
    user: str
    Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper identifier

    database: str
        Name of database where the data is harbored

    version: str
        String of number of data version

    backend: int
        ID of backend of the database in which the data is harbored 

    idspath: str
        IDS path (starting with IDS name) to the desired data to be collected (e.g 'equilibrium/time')

    pulses: list of tuples
        List of tuples containing (Pulse, Run)

    Returns
    -------
    pandas DataFrame
    """

    values = []
    idsname = idspath.split('/')[0]
    valpath = idspath[1 + len(idsname):]

    for entry in tqdm(pulses) if progbar else pulses:
        de = imas.DBEntry(backend, database, entry[0], entry[1], dbuser, version)
        de.open()
        try:
            value = de.partial_get(idsname, valpath)
            values.append(value)
        except Exception:
            values.append(None)

        de.close()

    df = pd.DataFrame(pulses, columns=['PULSE', 'RUN'])
    df['VALUE'] = values
    return df



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Extracts given quantities from all data entries of a given database", parents=[imas_parser])
    parser.add_argument("idspath", type=str, #nargs="*", #multiple paths not yet implemented
                        help="IDS path (starting with IDS name) to the desired data to be collected, e.g equilibrium/time")
    parser.add_argument("--saveas", type=str, help="File in which to store the results of this query, in csv format")
    parser.add_argument("--status", type=str, help="Will list only data entries with specified status (if such metadata is available)")
    parser.add_argument("--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    locpath = getDBPath(args.user, args.database, args.version)
    #if args.verbose:
    #    print(f"database located in {locpath}")

    backend = get_backend_id(args.backend)

    if backend==imasdef.MDSPLUS_BACKEND:
        pulses = mdsListPulseRun(locpath,with_status=args.status)
    elif backend==imasdef.HDF5_BACKEND:
        pulses = hdf5ListPulseRun(locpath)
    else:
        print(f"Functionality not yet implemented for backend {args.backend}")
        sys.exit()

    #if args.verbose:
    #    print(pulses)
        
    df = extract_from_db(args.user, args.database, args.version, backend, args.idspath, pulses)

    if args.saveas:
        if not Path(args.saveas).parent.exists():
            raise FileNotFoundError(
                "The path provided does not exist or has no such database file or directory. Please check spelling.")
        df.to_csv(args.saveas, na_rep='None', index=True, header=True)
    else:
        print(df.to_markdown())
