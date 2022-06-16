# Migrates IDS data from specified database to a desired folder, also converting data to desired backend

import imas
from imas import imasdef
import argparse
import pandas as pd
from idstools.cli import *
from pathlib import Path
from ids_extractor import mdsListPulseRun, hdf5ListPulseRun, getDBPath
from idstools.idsdiff import compare
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False

pd.set_option('display.max_rows', 90)

# Next steps: incorporate idschk function that validates ids. If validated then convert to HDF5.

parser = argparse.ArgumentParser(description='Copy all IDSs in given directory into a chosen one', parents=[imas_parser])
parser.add_argument("-do", "--database_out", type=str, default="migrations", help="Name of destination database")
parser.add_argument("-bo", "--backend_output", type=str, default="HDF5", help="Desired backend for destination data-entry (default=HDF5)")
parser.add_argument('ids', nargs='*', type=str, help='IDSs to copy (leave empty to select all IDSs with default occurrence, or append "/n" to copy a specific occurrence "n")')
args = parser.parse_args()

locpath = getDBPath(args.user, args.database, args.version)

backend = get_backend_id(args.backend)

log = []

if backend == imas.imasdef.MDSPLUS_BACKEND:
    files = mdsListPulseRun(locpath)
elif backend == imas.imasdef.HDF5_BACKEND:
    files = hdf5ListPulseRun(locpath)

if args.ids == []:
    args.ids = [ids.value for ids in list(imas.IDSName)]

for pulse in tqdm(files) if progbar else files:
    idsinf = []
    run = pulse[1]
    src = imas.DBEntry(backend, args.database, pulse[0], run, args.user)
    src.open()
    dest = imas.DBEntry(get_backend_id(args.backend_output), args.database_out, pulse[0], run)
    dest.create()
    for idsname in args.ids:
        inocc = 0
        idsid = idsname.split('/')
        if len(idsid) == 2:
            inocc = int(idsid[1])

        idsobj = src.get(idsid[0], occurrence=inocc)
        if idsid[0] == 'dataset_description':
            idsobj.dd_version = os.environ['IMAS_VERSION']
        try:
            if idsobj.ids_properties.homogeneous_time != imas.imasdef.EMPTY_INT:
                inocc
                dest.put(idsobj, occurrence=inocc)
                idsobj2 = dest.get(idsid[0], occurrence=inocc)
                idsinf.append((idsname, compare(idsobj, idsobj2, verb=False)))
        except Exception as exc:
            print(str(exc), file=sys.stderr)
    log.append(idsinf)

    src.close()
    dest.close()

df = pd.DataFrame(files, columns=['PULSE', 'RUN'])
df['IDS STATUS'] = log
print(df)
