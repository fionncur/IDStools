# From IDS to readable CSV
import imas
import os
from imas import imasdef
import pandas as pd
import argparse
from pathlib import Path
from idstools.cli import *
import yaml
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False



    
def get_status(path):
    """ Function that returns the status in the given yaml file
    Parameter
    ---------
    path: str or Path
    """
    p = Path(path)
    try:
        with open(p,"r") as f:
            metadata = yaml.safe_load(f)
    except FileNotFoundError as exc:
        print(exc)
        return 'unknown'
    return metadata['status']
    



def mdsListPulseRun(locpath, with_status=None):
    """ Function that lists Pulse and Run numbers from a given database, in MDSPLUS
    Parameter
    ---------
    locpath: str or Path
        Path in which the database files are stored
    
    Returns
    -------
    list of tuple (pulse,run) 
    """
    locpath = Path(locpath).expanduser()
    if not locpath.exists():
        raise FileNotFoundError("The path provided does not exist or has no such database file or directory. Please check spelling.")
    pulses = []
    folder = Path(locpath).glob('**/*.datafile')
    for entry in folder:
        if (with_status is None) or (with_status==get_status(entry.with_suffix(".yaml"))):
            file = str(entry).split('/')[-1].split('_')[1].split('.')[0]
            if len(file) <= 4:
                pulse = 0
            else:
                pulse = int(file[0:-4])
            run = int(file[-4:]) + 10000 * int(str(entry).split('/')[-2])
            pulses.append((pulse, run))
    return pulses


def hdf5ListPulseRun(locpath):
    """ Function that lists Pulse and Run numbers from a given database, in HDF5
    Parameter
    ---------
    locpath: str or Path
           Path in which the database files are stored
    with_status: str
        If set, will list only pulses with given status (in associated yaml file, e.g. 'obsolete', 'active')

    Returns
    -------
    list of tuple (pulse,run) 
    """
    locpath = Path(locpath).expanduser()
    if not locpath.exists():
        raise FileNotFoundError("The path provided does not exist or has no such database file or directory. Please check spelling.")
    pulses = []
    folder = Path(locpath).glob('**/*master.h5')
    for entry in folder:
        pulse = int(str(entry).split('/')[-3])
        run = int(str(entry).split('/')[-2])
        pulses.append((pulse, run))
    return pulses


def getDBPath(user, database, version):
    """ Function that returns a pathlib Path to desired database, depending on the user, database and version names.
    Parameters
    ---------
    user: str
        Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper identifier

    database: str
        Name of database where the data is harbored

    version: str
        String of number of data version

    Returns
    -------
    pathlib.Path
    """
    if user == 'public':
        locpath = Path(os.environ['IMAS_HOME'] + '/shared/imasdb/' + database + "/" + version)
    else:
        locpath = Path(os.path.expanduser('~' + user) + "/public/imasdb/" + database + "/" + version)
    return locpath


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.",
                                     parents=[imas_parser])
    parser.add_argument("idspath", type=str, help="IDS path (starting with IDS name) to the desired data to be collected, e.g equilibrium/time")
    parser.add_argument("--saveas", type=str, help="Path to directory ending with name of file to save retrieved data")
    parser.add_argument("-i", "--index", action="store_true", help="Should index be shown in final .csv file?")
    parser.add_argument("-V","--Verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()
    database = args.database
    idspath = args.idspath

    locpath = getDBPath(args.user, database, args.version)

    idsname = idspath.split('/')[0]
    valpath = idspath[1 + len(idsname):]

    values = []

    backend = get_backend_id(args.backend)

    if backend == imas.imasdef.MDSPLUS_BACKEND:
        pulses = mdsListPulseRun(locpath)
    elif backend == imas.imasdef.HDF5_BACKEND:
        pulses = hdf5ListPulseRun(locpath)

        
    for entry in tqdm(pulses) if progbar else pulses:
        de = imas.DBEntry(backend, database, entry[0], entry[1], args.user, args.version)
        de.open()
        try:
            value = de.partial_get(idsname, valpath)
            values.append(value)
        except Exception:
            values.append(None)

        de.close()

    df = pd.DataFrame(pulses, columns=['PULSE', 'RUN'])
    df['VALUE'] = values

    if args.Verbose or not args.saveas:
        print(df)
    
    if args.saveas:
        if not Path(args.saveas).parent.exists():
            raise FileNotFoundError("The path provided does not exist or has no such database file or directory. Please check spelling.")
        saveresultsin = Path(r'' + args.saveas + '.csv')
        df.to_csv(saveresultsin, na_rep='None', index=args.index, header=True)
