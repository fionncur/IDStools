#!/usr/bin/env python

import argparse
import inspect
import logging
import os
import sys

import imas
import numpy as np

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)


from idstools.cli import imas_parser
from idstools.helper import setup_logger

logger = setup_logger("module", logging.WARN)
np.set_printoptions(threshold=1, precision=2, suppress=True)


def getAvailableIdsAndTimes(idsObject: imas.ids) -> list:
    """
    This function retrieves available IDs and their corresponding time arrays from an IDS object.

    Args:
        idsObject (imas.ids): The `idsObject` parameter is an object of the `imas.ids` class, which is used to access idses. This function takes this object as input and returns a list of tuples containing available IDS names and their corresponding time arrays.

    Returns:
        a list of tuples, where each tuple contains an IDS name and an array of times associated with that IDS.
    """

    def idsProperties(obj):
        try:
            obj.__getattribute__("ids_properties")
            return True
        except Exception:
            return False

    predicateIdsProperties = lambda x: idsProperties(x)
    idsWithPropertiesDict = inspect.getmembers(idsObject, predicateIdsProperties)
    result = []
    for _idsName, idsPropertiesObject in idsWithPropertiesDict:
        try:
            maxOccurrences = idsPropertiesObject.getMaxOccurrences()

        except AttributeError:
            maxOccurrences = 1
        for occurrence in range(maxOccurrences + 1):
            idsName = _idsName if occurrence == 0 else f"{_idsName}/{str(occurrence)}"
            try:
                (_, timeArray) = idsObject.getTimes(idsName)
            except Exception as exc:
                timeArray = []
                logger.critical(
                    f"ERROR! IDS {idsName} : Reading time array fails due to following problem : {exc}"
                )
            if timeArray is not None and len(timeArray):
                result.append((idsName, timeArray))
    return result


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
