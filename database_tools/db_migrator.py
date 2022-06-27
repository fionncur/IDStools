# Migrates IDS data from specified database to a desired folder, also converting data to desired backend

import imas
from imas import imasdef
import os
import argparse
import pandas as pd
from idstools.cli import *
from pathlib import Path
from ids_extractor import mdsListPulseRun, hdf5ListPulseRun, getDBPath
from idschk import ids_validator
from idstools.idsdiff import compare
from idstools.idslist import available_in_dbentry
from datetime import datetime
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False


parser = argparse.ArgumentParser(description='Copy all IDSs in given directory into a chosen one', parents=[imas_parser])
parser.add_argument("-do", "--database_out", type=str, default="migrations", help="Name of destination database")
parser.add_argument("-bo", "--backend_output", type=str, default="HDF5", help="Desired backend for destination data-entry (default=HDF5)")
args = parser.parse_args()

locpath = getDBPath(args.user, args.database, args.version)

backend = get_backend_id(args.backend)

log = []

if backend == imas.imasdef.MDSPLUS_BACKEND:
    files = mdsListPulseRun(locpath)
elif backend == imas.imasdef.HDF5_BACKEND:
    files = hdf5ListPulseRun(locpath)

for pulse in tqdm(files) if progbar else files:
    idsinf = []
    run = pulse[1]
    src = imas.DBEntry(backend, args.database, pulse[0], run, args.user)
    src.open()
    dest = imas.DBEntry(get_backend_id(args.backend_output), args.database_out, pulse[0], run)
    dest.create()
    for ids in available_in_dbentry(src):
        idsname = ids[0]
        inocc = ids[1]
        idsobj = src.get(idsname, occurrence=inocc)
        if idsname == 'dataset_description':
            idsobj.dd_version = os.environ['IMAS_VERSION']
        try:
            if idsobj.ids_properties.homogeneous_time != imas.imasdef.EMPTY_INT:
                dest.put(idsobj, occurrence=inocc)
                idsobj2 = dest.get(idsname, occurrence=inocc)
                idsinf.append((idsname, compare(idsobj, idsobj2, verb=False), ids_validator(idsobj, 'required_fields_core.yml')[0]))
        except Exception as exc:
            print(str(exc), file=sys.stderr)
    log.append(idsinf)

    src.close()
    dest.close()

df = pd.DataFrame(files, columns=['PULSE', 'RUN'])
df['IDS STATUS | Validation'] = log

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
df.to_csv(args.database_out + " migration_log--" + date + ".csv", na_rep='None', index=False, header=True)
