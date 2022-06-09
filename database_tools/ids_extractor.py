# From Rosetta to IDS to readable CSV
import imas
from imas import imasdef
import pandas as pd
import argparse
from pathlib import Path
from idstools.cli import get_backend_id

parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.")
parser.add_argument("--user", type=str, default="hoeneno", help="User harboring desired data")
parser.add_argument("--database", type=str, default="benchmark", help="Database harboring desired data")
parser.add_argument("--version", type=str, default="3", help="Version of IMAS database")
parser.add_argument("--idspath", type=str, default="summary/global_quantities/ip/value", help="IDS path to desired data to be collected ")
parser.add_argument("--backend", type=str, default="HDF5", help="Desired backend of use (will read MDSPLUS, HDF5, or both")
args = parser.parse_args()
database = args.database
idspath = args.idspath
backend = args.backend.upper()
locpath = "/home/ITER/" + args.user + "/public/imasdb/" + database + "/" + args.version
shots = []
runs = []
values = []
backends = []

idsname = idspath.split('/')[0]
valpath = idspath.split('/')[1:]


# MDS+

if backend == 'MDSPLUS' or backend == 'MDS+' or backend == backend == "BOTH":
    folder = Path(locpath).glob('**/*.datafile')
    for entry in folder:
        file = str(entry).split('/')[-1].split('_')[1].split('.')[0]
        if len(file) <= 4:
            shot = 0
        else:
            shot = int(file[0:-4])
        run = int(file[-4:])+10000*int(str(entry).split('/')[-2])
        de = imas.DBEntry(get_backend_id(args.backend), database, shot, run)
        de.open()
        value = de.partial_get(idsname, valpath)
        shots.append(shot)
        runs.append(run)
        values.append(value)
        de.close()
        backends.append('MDSPLUS')


# HDF5

if backend == 'HDF5' or backend == "BOTH":
    folder = Path(locpath).glob('**/*master.h5')
    for entry in folder:
        shot = int(str(entry).split('/')[-3])
        run = int(str(entry).split('/')[-2])
        shots.append(shot)
        runs.append(run)
        print(str(get_backend_id(args.backend)) + ' ' + str(database) + ' ' + str(shot) + ' ' + str(run))
        de = imas.DBEntry(get_backend_id(args.backend), database, shot, run)
        de.open()
        value = de.partial_get(idsname, valpath)
        values.append(value)
        de.close()
        backends.append('HDF5')


df = pd.DataFrame(list(zip(shots, runs, backends)), columns=['SHOT', 'RUN', 'VALUE', 'BACKEND'])
print(df)

# df.to_csv(r'C:\users\vidalm\Work Folders\Desktop\export_dataframe.csv', index=False, header=True)
