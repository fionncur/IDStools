#!/usr/bin/env python

import argparse
import os
import sys

import imas
import numpy as np

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)


from idstools.utils.idshelper import (
    getAvailableIdsAndTimes,
    getAvailableIdsAndOccurrences,
)
from idstools.utils.idslogger import setupLogger
from idstools.utils.clihelper import getBackendID, imasParser

logger = setupLogger("module")
np.set_printoptions(threshold=1, precision=2, suppress=True)


parser = argparse.ArgumentParser(
    description="---- List available IDSes in the pulse",
    parents=[imasParser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)
parser.add_argument(
    "-y",
    "--yaml-format",
    action="store_true",
    dest="yaml_format",
    help="List ids content for yaml files aimed at describing a scenario",
)

args = parser.parse_args()

if args.yaml_format:
    # Open the database and read the necessary IDSs
    connection = imas.DBEntry(
        getBackendID(args.backend), args.database, args.shot, args.run, args.user
    )
    status, _ = connection.open()

    if status != 0:
        logger.error(
            f"Shot {str(args.shot)}, run {str(args.run)} for user_or_path = {args.user} and database = {args.database} does not exist",
        )
        exit()

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

else:
    idsObject = imas.ids(
        args.shot,
        args.run,
    )
    print(args.user)
    err, _ = idsObject.open_env(args.user, args.database, args.version)
    if err != 0:
        logger.critical(
            f"Shot {args.shot}, run {args.run} for user {args.user} and database {args.database} is not reachable ----> abort!",
        )
        sys.exit(err)

    availableIdsAndTimes = getAvailableIdsAndTimes(idsObject)
    question_string = "?"
    for idsName, timeArray in availableIdsAndTimes:
        if len(timeArray) == 1 and np.isnan(timeArray[0]):
            print(f"{idsName:15}:  {question_string:5} slices: heterogeneous IDS ")
        elif len(timeArray) == 1 and timeArray[0] == np.NINF:
            print(f"{idsName:15}:  {question_string:5} slices: time independent IDS ")
        else:
            print(f"{idsName:15}: {str(len(timeArray)):5} slices: {timeArray} ")
