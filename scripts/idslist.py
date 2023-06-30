#!/usr/bin/env python

import argparse
import os
import sys

import imas
import numpy as np

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)


from idstools.utils.clihelper import imas_parser
from idstools.utils.idshelper import getAvailableIdsAndTimes
from idstools.utils.idslogger import setup_logger

logger = setup_logger("module")
np.set_printoptions(threshold=1, precision=2, suppress=True)  


parser = argparse.ArgumentParser(
    description="---- List available IDSes in the pulse",
    parents=[imas_parser],
)
parser.add_argument("-s", "--shot", help="Shot number", required=True, type=int)
parser.add_argument("-r", "--run", help="Run number", required=True, type=int)

args = parser.parse_args()


idsObject = imas.ids(  
    args.shot,
    args.run,
)

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
