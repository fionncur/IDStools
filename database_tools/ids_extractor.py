# From Rosetta to IDS to readable CSV
import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.")
parser.add_argument("--path", type=str, default="/home/ITER/hoeneno/public/imasdb/benchmark/3", help="Path to database containing desired shots and runs")
# parser.add_argument("--backend", type=str, default="HDF5", help="Desired backend of use (currently supports MDS+ or HDF5")
args = parser.parse_args()
path = args.path
# backend = args.backend

shots = []
runs = []
backends = []

# MDS+

folder = Path(path).glob('**/*.datafile')
for entry in folder:
    file = str(entry).split('/')[-1].split('_')[1].split('.')[0]
    if len(file) <= 4:
        shot = 0
    else:
        shot = int(file[0:-4])
    run = int(file[-4:])+10000*int(str(entry).split('/')[-2])
    shots.append(shot)
    runs.append(run)
    backends.append('MDSPLUS')


# HDF5

folder = Path(path).glob('**/*master.h5')
for entry in folder:
    shot = int(str(entry).split('/')[-3])
    run = int(str(entry).split('/')[-2])
    shots.append(shot)
    runs.append(run)
    backends.append('HDF5')


df = pd.DataFrame(list(zip(shots, runs, backends)), columns=['SHOT', 'RUN', 'BACKEND'])
print(df)


# df.to_csv(r'C:\users\vidalm\Work Folders\Desktop\export_dataframe.csv', index=False, header=True)


# Path to folder, I need to explore in this folder if I can find and list all available shot and run numbers of IDS entries for given backend
