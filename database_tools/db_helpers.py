from pathlib import Path
from glob import glob 
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
        with open(p, "r") as f:
            metadata = yaml.safe_load(f)
    except FileNotFoundError as exc:
        print(exc)
        return 'unknown'
    return metadata['status']
    



def mdsListPulseRun(locpath, with_status=None):
    """ Function that lists Pulse and Run numbers from a given database, in MDSPLUS

    Parameters
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
    # folder = Path(locpath).glob('**/*.datafile') # --> does not work with linked subfolders (https://bugs.python.org/issue33428)
    folder = glob(str(locpath)+"/**/*.datafile", recursive=True)
    for entry in folder:
        if (with_status is None) or (with_status == get_status(Path(entry).with_suffix(".yaml"))):
            file = entry.split('/')[-1].split('_')[1].split('.')[0]
            if len(file) <= 4:
                pulse = 0
            else:
                pulse = int(file[0:-4])
            run = int(file[-4:]) + 10000 * int(entry.split('/')[-2])
            pulses.append((pulse, run))
    return pulses


def hdf5ListPulseRun(locpath):
    """ Function that lists Pulse and Run numbers from a given database, in HDF5

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
    #folder = Path(locpath).glob('**/*master.h5')
    folder = glob(str(locpath)+"/**/*master.h5", recursive=True)
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
