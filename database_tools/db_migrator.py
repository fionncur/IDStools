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
parser.add_argument("--validate", action="store_true", help="Performs diff and validation of the migrated data")
args = parser.parse_args()

locpath = getDBPath(args.user, args.database, args.version)

backend = get_backend_id(args.backend)

log = []

if backend == imas.imasdef.MDSPLUS_BACKEND:
    files = mdsListPulseRun(locpath)
elif backend == imas.imasdef.HDF5_BACKEND:
    files = hdf5ListPulseRun(locpath)

for pulse in files: #tqdm(files) if progbar else files:
    idsinf = []
    run = pulse[1]
    src = imas.DBEntry(backend, args.database, pulse[0], run, args.user)
    src.open()
    dest = imas.DBEntry(get_backend_id(args.backend_output), args.database_out, pulse[0], run)
    dest.create()
    avids = available_in_dbentry(src)
    for ids in tqdm(avids, desc=f"Pulse {pulse}") if progbar else avids:
        idsname = ids[0]
        inocc = ids[1]
        idsobj = src.get(idsname, occurrence=inocc)
        dest.put(idsobj, occurrence=inocc)

        if args.validate:
            idsobj2 = dest.get(idsname, occurrence=inocc)
            same = compare(idsobj, idsobj2, verb=False)
            idsinf.append((idsname,same,ids_validator(idsobj,os.path.abspath(os.path.dirname( __file__ ))+'/required_fields_core.yml')[0]))
            #del idsobj2

        #del idsobj

    src.close()
    #del src
    dest.close()
    #del dest
        
    log.append(idsinf)


df = pd.DataFrame(files, columns=['PULSE', 'RUN'])
df['IDS STATUS | Validation'] = log

date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
df.to_csv(args.database_out + " migration_log--" + date + ".csv", na_rep='None', index=False, header=True)
