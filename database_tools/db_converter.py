#!/usr/bin/env python
# Converts an IMAS database (all its data-entries) to the specified folder and backend

import imas
from imas import imasdef
import os
import argparse
import pandas as pd
from idstools.utils.clihelper import getBackendID, imasParser
from pathlib import Path
from database_tools.db_helpers import mdsListPulseRun, hdf5ListPulseRun, getDBPath
from database_tools.idschk import ids_validator
from idstools.idsdiff import compare
from idstools.idslist import available_in_dbentry
from datetime import datetime
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False


parser = argparse.ArgumentParser(description='Copy all data-entries from one database into another one', parents=[imasParser])
parser.add_argument("-do", "--database_out", type=str, required=True, help="Name of destination database")
parser.add_argument("-bo", "--backend_output", type=str, required=True, help="Desired backend for destination data-entry")
parser.add_argument("--skip-obsolete", action="store_true", help="Do not copy data that have been marked obsolete (ITER scenarios only)")
parser.add_argument("--validate", action="store_true", help="Performs diff and validation of the migrated data")
args = parser.parse_args()

locpath = getDBPath(args.user, args.database, args.version)

backend = getBackendID(args.backend)

log = []

if backend == imas.imasdef.MDSPLUS_BACKEND:
    files = mdsListPulseRun(locpath, with_status='active' if args.skip_obsolete else None)
elif backend == imas.imasdef.HDF5_BACKEND:
    files = hdf5ListPulseRun(locpath)

for pulse in tqdm(files) if progbar else files:
    idsinf = []
    run = pulse[1]
    src = imas.DBEntry(backend, args.database, pulse[0], run, args.user)
    src.open()
    dest = imas.DBEntry(getBackendID(args.backend_output), args.database_out, pulse[0], run)
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
            idsinf.append((idsname, same, ids_validator(idsobj, os.path.abspath(os.path.dirname(__file__))+'/required_fields_core.yml')[0]))

    src.close()
    dest.close()
        
    log.append(idsinf)


if args.validate:    
    df = pd.DataFrame(files, columns=['PULSE', 'RUN'])
    df['IDS STATUS | Validation'] = log
    date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
    df.to_csv(args.database_out + " migration_log--" + date + ".csv", na_rep='None', index=False, header=True)
