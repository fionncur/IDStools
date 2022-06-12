# From IDS to readable CSV
import imas
import os
from imas import imasdef
import pandas as pd
import argparse
from pathlib import Path
from idstools.cli import get_backend_id
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False


# Function that lists Pulse and Run numbers from given database, in MDSPLUS

def mdsListPulseRun(locpath):
    if not locpath.exists():
        print("No such database file or directory. Please check spelling.")
        exit()
    pulses = []
    folder = Path(locpath).glob('**/*.datafile')
    for entry in folder:
        file = str(entry).split('/')[-1].split('_')[1].split('.')[0]
        if len(file) <= 4:
            pulse = 0
        else:
            pulse = int(file[0:-4])
        run = int(file[-4:]) + 10000 * int(str(entry).split('/')[-2])
        pulses.append((pulse, run))
    return pulses


# Function that lists Pulse and Run numbers from given database, in HDF5

def hdf5ListPulseRun(locpath):
    if locpath.exists():
        print("No such database file or directory. Please check spelling.")
        exit()
    pulses = []
    folder = Path(locpath).glob('**/*master.h5')
    for entry in folder:
        pulse = int(str(entry).split('/')[-3])
        run = int(str(entry).split('/')[-2])
        pulses.append((pulse, run))
    return pulses



parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.")
parser.add_argument("--user", type=str, default="", help="User harboring desired data, or public option")
parser.add_argument("--database", type=str, default="", help="Database harboring desired data")
parser.add_argument("--version", type=str, default="3", help="Version of IMAS database")
parser.add_argument("--idspath", type=str, default="", help="IDS path to desired data to be collected")
parser.add_argument("--saveas", type=str, default="", help="Path to directory ending with name of file to save retrieved data")
parser.add_argument("--backend", type=str, default="HDF5", help="Desired backend of use (will read MDSPLUS, HDF5, or both")
parser.add_argument("--index", type=str, default="True", help="Should index be shown in final .csv file?")
args = parser.parse_args()
database = args.database
idspath = args.idspath
backend = args.backend.upper()

idsname = idspath.split('/')[0]
valpath = idspath[1 + len(idsname):]
if args.user == 'public':
    locpath = Path(os.environ['IMAS_HOME'] + '/shared/imasdb/' + database + "/" + args.version)
else:
    locpath = Path(os.path.expanduser('~' + args.user) + "/public/imasdb/" + database + "/" + args.version)

values = []

if not Path(args.saveas).parent.exists():
    print("No such file or directory to save the results. Please check spelling")
    exit()

# Retrieve data in MDSPLUS

if backend == 'MDSPLUS' or backend == 'MDS+' or backend == "BOTH":
    pulses = mdsListPulseRun(locpath)
    for entry in tqdm(pulses):
        # get_backend_id(backend) manually entered. If code wishes to be generalized with get_backend_id(backend), 'MDS+' and 'BOTH' options cannot be used.
        de = imas.DBEntry(12, database, entry[0], entry[1], args.user, args.version)
        de.open()
        value = de.partial_get(idsname, valpath)
        de.close()
        values += value,

# Retrieve data in HDF5

if backend == 'HDF5' or backend == "BOTH":
    pulses = hdf5ListPulseRun(locpath)
    for entry in tqdm(pulses):
        de = imas.DBEntry(13, database, entry[0], entry[1], args.user, args.version)
        de.open()
        value = de.partial_get(idsname, valpath)
        de.close()
        values += value,


df = pd.DataFrame(pulses, columns=['PULSE', 'RUN'])
df['VALUE'] = values
saveresultsin = Path(r'' + args.saveas + '.csv')
if args.index.upper == 'FALSE' or args.index.upper() == 'NO':
    index = False
else:
    index = True
df.to_csv(saveresultsin, index=index, header=True)
