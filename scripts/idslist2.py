#!/usr/bin/env python

import argparse
import logging
import os
import sys

import imas

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)

from idstools.utils.clihelper import get_backend_id, imas_parser
from idstools.utils.idslogger import setup_logger
from idstools.utils.idshelper import getAvailableIdsAndOccurrences

logger = setup_logger("module")


# Management of input arguments
parser = argparse.ArgumentParser(
    description="---- List ids content for yaml files aimed at describing a scenario ----",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="run number", required=True, type=int)
args = parser.parse_args()

# Open the database and read the necessary IDSs
connection = imas.DBEntry(
    get_backend_id(args.backend), args.database, args.shot, args.run, args.user
)
status, _ = connection.open()

if status != 0:
    logger.error(
        f"Shot {str(args.shot)}, run {str(args.run)} for user_or_path = {args.user} and database = {args.database} does not exist",
    )
    exit()

# Print IDS contents
for idsname, oc in getAvailableIdsAndOccurrences(connection):
    homogeneous_time = connection.partial_get(
        idsname, "ids_properties/homogeneous_time", occurrence=oc
    )
    times = connection.partial_get(idsname, "time", occurrence=oc)

    # Format idsname
    idsnameoc = f"{idsname}/{str(oc)}" if oc > 0 else idsname
    # For every homogeneous_time [0,1,2]
    if homogeneous_time == 0:
        print(f"  {idsnameoc}:")
        print(f"     time_step_number: {len(times)}")
        print("     time:             [unhomogeneous]")
    elif homogeneous_time == 1:
        if len(times) > 1:
            time_step = (times[len(times) - 1] - times[0]) / (len(times) - 1)
            start_time = times[0]
            end_time = times[len(times) - 1]
            print(f"  {idsnameoc}:")
            print(f"     time_step_number: {len(times)}")
            print(
                f"     start_end_step:   [{str(start_time)} {str(end_time)} {str(time_step)}]"
            )
        elif len(times) == 1:
            print(f"  {idsnameoc}:")
            print(f"     time_step_number: {len(times)}")
            print(f"     time:             [{str(times[0])}]")
    elif homogeneous_time == 2:
        print(f"  {idsnameoc}:")
        print(f"     time_step_number: {len(times)}")
        print("     time:             [static]")
