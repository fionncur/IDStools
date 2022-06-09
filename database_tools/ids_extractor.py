# From Rosetta to IDS to readable CSV
import pandas as pd
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="This script applies conversion of IDS data into readable CSV files.")
parser.add_argument("--path", type=str, default="/home/ITER/vidalm/public/imasdb/test/3/0", help="Path to database containing desired shots and runs")
args = parser.parse_args()
path = args.path

folder = Path(path).glob('**/*.datafile')
shots = []
runs = []
for entry in folder:
    file = str(entry).split('/')[9].split('_')[1].split('.')[0]
    shot = file[0:-4]
    run = file[-4:]
    shots.append(shot)
    runs.append(run)

df = pd.DataFrame(list(zip(shots, runs)), columns=['SHOT', 'RUN'])
print(df)


# df.to_csv(r'C:\users\vidalm\Work Folders\Desktop\export_dataframe.csv', index=False, header=True)


# Path to folder, I need to explore in this folder if I can find and list all available shot and run numbers of IDS entries for given backend
