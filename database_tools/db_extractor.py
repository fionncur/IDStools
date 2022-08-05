# Return values of an IDS in all data entries of a database

import imas
import os
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





def extract_from_db(user, database, version, backend, idspath, pulses):
    """ Function that returns a pandas dataframe displaying all values of given IDSs extracted by the function.

    Parameters
    ---------
    user: str
    Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper identifier

    database: str
        Name of database where the data is harbored

    version: str
        String of number of data version

    backend: str
        Name of backend of the database in which the data is harbored (currently supports only MDSPLUS and HDF5)

    idspath: str
        IDS path (starting with IDS name) to the desired data to be collected (e.g 'equilibrium/time')

    pulses: list of tuples
        List of tuples containing (Pulse, Run)

    Returns
    -------
    pandas DataFrame
    """

    values = []
    backend = get_backend_id(backend)
    idsname = idspath.split('/')[0]
    valpath = idspath[1 + len(idsname):]

    for entry in tqdm(pulses) if progbar else pulses:
        de = imas.DBEntry(backend, database, entry[0], entry[1], user, version)
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

    parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.", parents=[imas_parser])
    parser.add_argument("idspath", type=str, nargs="*", help="IDS path(s) (starting with IDS name) to the desired data to be collected, e.g equilibrium/time")
    parser.add_argument("--saveas", type=str, help="Path to directory ending with name of file to save retrieved data")
    parser.add_argument("-i", "--index", action="store_true", help="Should index be shown in final .csv file?")
    parser.add_argument("-verb", "--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()
    database = args.database
    idspath = args.idspath

    locpath = getDBPath(args.user, args.database, args.version)

    df = extract_from_db(args.user, args.database, args.version, args.backend, args.idspath, pulses=mdsListPulseRun(locpath) if args.backend == imas.imasdef.MDSPLUS_BACKEND else hdf5ListPulseRun(locpath))

    if args.verbose or not args.saveas:
        print(df)

    if args.saveas:
        if not Path(args.saveas).parent.exists():
            raise FileNotFoundError(
                "The path provided does not exist or has no such database file or directory. Please check spelling.")
        saveresultsin = Path(r'' + args.saveas + '.csv')
        df.to_csv(saveresultsin, na_rep='None', index=args.index, header=True)
