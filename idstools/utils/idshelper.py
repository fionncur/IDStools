"""
This module 

"""

import inspect
import logging
import time
import types

import imas
import numpy as np
import pandas as pd
from packaging import version

logger = logging.getLogger("module")
ARRAY_EQUAL_KWARGS = (
    "equal_nan=True" if version.parse(np.__version__) > version.parse("1.19") else ""
)
progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Install tqdm to enable progress bar")
    progbar = False


def isIdsField(idstype: type) -> bool:
    """
    This function checks if a given type is a possible field of an IDS.

    Args:
        idstype (type): The type of an attribute from an IDS or a substructure of an IDS.

    Returns:
        The function isIdsField returns a boolean value indicating whether the passed type is a possible  field of an IDS or not.
    """
    return (
        idstype != types.MethodType
        and idstype != types.FunctionType
        and "Logger" not in str(idstype)
        and "HLIUtils" not in str(idstype)
    )


def getIdsAttributes(idsobj: object) -> list:
    """
    This function returns a list of attribute names for a given IDS object.

    Args:
        idsobj (object): The IDS or substructure object for which the function will return a list of attribute names.

    Returns:
        The function `getIdsAttributes` returns a list of attribute names for the given IDS object which are not private and are ids fields.
    """
    if "imas" in str(type(idsobj)):
        return [
            a[0]
            for a in inspect.getmembers(idsobj)
            if not a[0].startswith("_") and isIdsField(type(a[1]))
        ]
    else:
        return []


def getIDSSize(dbEntryObject: imas.DBEntry, idsNames=None) -> dict:
    """
    The function `getIDSSize` retrieves the size of IDS objects from a database entry and returns a dictionary containing the size in bytes and the time taken to read each object.

    Args:
        dbEntryObject (imas.DBEntry): The `dbEntryObject` parameter is an object of type `imas.DBEntry`. It is used to access the data in the IMAS database.
        idsNames: idsNames is a list of IDS names. If it is not provided, it defaults to None.

    Returns:
        a dictionary containing information about the size and time taken to read IDS objects from a database entry. The dictionary has the following structure:
    """
    if idsNames is None:
        idsNames = [i.value for i in imas.IDSName]
    if type(idsNames) is str:
        idsNames = idsNames.split(",")
    idsSizeDict = {}
    for idsName in idsNames:
        occurrencesCount = eval(f"imas.{idsName}.getMaxOccurrences()")
        for o in range(occurrencesCount + 1):
            homogeneousTime = dbEntryObject.partial_get(
                idsName, "ids_properties/homogeneous_time", occurrence=o
            )
            if homogeneousTime >= 0:
                field = f"{idsName}/{o}"
                idsSizeDict[field] = {}
                startTime = time.time()
                idsObject = dbEntryObject.get(idsName, occurrence=o)
                idsSizeDict[field]["time"] = time.time() - startTime
                idsSizeDict[field]["bytes"] = getObjectSize(idsObject)
                print(
                    "Reading %0.3f MB of data for %s took %0.2f seconds"
                    % (
                        idsSizeDict[field]["bytes"] / 1024**2,
                        field,
                        idsSizeDict[field]["time"],
                    )
                )
                del idsObject
    return idsSizeDict


def getAllIDSSize(dbEntryObject: imas.DBEntry):
    """
    The function `getAllIDSSize` calculates the total size in bytes of all IDS in a given `dbEntryObject`.

    Args:
        dbEntryObject (imas.DBEntry): The parameter `dbEntryObject` is of type `imas.DBEntry`.

    Returns:
        the total size in bytes of all the IDS in the given `dbEntryObject`.
    """
    idsSizeDict = getIDSSize(dbEntryObject)
    totalBytes = np.array([ids["bytes"] for ids in idsSizeDict.values()]).sum()
    return totalBytes


def getAllIDSGetTime(dbEntryObject: imas.DBEntry):
    """
    The function `getAllIDSGetTime` calculates the total time for all IDS in a given `dbEntryObject`.

    Args:
        dbEntryObject (imas.DBEntry): The parameter `dbEntryObject` is of type `imas.DBEntry`.

    Returns:
        the total time to get all the IDSes in the given `dbEntryObject`.
    """
    idsSizeDict = getIDSSize(dbEntryObject)
    return np.array([ids["time"] for ids in idsSizeDict.values()]).sum()


def getObjectSize(obj: object) -> int:
    objectSize = 0
    if type(obj) == str:
        objectSize += len(obj)
    elif type(obj) == np.ndarray:
        objectSize += obj.nbytes
    elif type(obj) == int:
        objectSize += 4
    elif type(obj) == float:
        objectSize += 8
    elif type(obj) == list:
        for objItem in obj:
            objectSize += getObjectSize(objItem)
    elif type(obj) == dict:
        for objValue in obj.values():
            objectSize += getObjectSize(objValue)
    else:
        for objValue in obj.__dict__.values():
            objectSize += getObjectSize(objValue)
    return objectSize


def getIdsTypes():
    """
    This function returns list of strings corresponding to all ids types for each IDSName object in the imas module.

    Returns:
        The function `getIdsTypes()` is returning a list of values of all the `value` attributes of the `IDSName` objects in the `imas` module.
    """
    return [ids.value for ids in list(imas.IDSName)]


def getAvailableIdsAndOccurrences(dbEntryObject: imas.DBEntry, time_mode=None):
    """
    This function returns a list of pairs of available IDS types and their occurrences in a given DBEntry object.

    Args:
        dbEntryObject (imas.DBEntry): An object of the class imas.DBEntry, which represents an open DBEntry in which available IDSs will be looked for.
        time_mode: The time mode of interest for the IDSs in the given DBEntry. It can be one of the following values:(imas.imasdef.IDS_TIME_MODE_HETEROGENEOUS, IDS_TIME_MODE_HOMOGENEOUS or IDS_TIME_MODE_INDEPENDENT)

    Returns:
        a list of pairs (idstype:str,occurrence:int) with data in the given DBEntry.
    """
    availableidslist = []
    for idstype in getIdsTypes():
        for occ in range(getattr(imas, idstype)().getMaxOccurrences()):
            homogeneous_time = dbEntryObject.partial_get(
                idstype, "ids_properties/homogeneous_time", occurrence=occ
            )
            if homogeneous_time != imas.imasdef.EMPTY_INT and (
                time_mode is None or time_mode == homogeneous_time
            ):
                availableidslist.append((idstype, occ))
    return availableidslist


def getAvailableIdsAndTimes(idsObject: imas.ids) -> list:
    """
    This function retrieves available IDs and their corresponding time arrays from an IDS object.

    Args:
        idsObject (imas.ids): The `idsObject` <class 'imas.ids.ids'> parameter is an object of the `imas.ids` class, which is used to access idses. This function takes this object as input and returns a list of tuples containing available IDS names and their corresponding time arrays.

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


def resampleIndices(
    dbin: str, dbout: str, idsname: str, start: int = 0, stop: int = None, step: int = 1
):
    """
    The function resampleIndices takes in a database input, database output, and an idsname, and resamples the data based on the specified start, stop, and step values.

    Args:
        dbin (str): The parameter "dbin" is a string that represents the input database name. It is the database from which the data will be read.
        dbout (str): The parameter `dbout` is a string that represents the name of the output database. It is the database where the resampled data will be stored.
        idsname (str): The parameter "idsname" is a string that represents the ids that you want to resample.
        start (int): The start parameter is the index of the first time value to be resampled.
        stop (int): The `stop` parameter is used to specify the index at which the resampling should stop. If `stop` is not provided, the resampling will continue until the end of the `times` array.
        step (int): The `step` parameter determines the interval between the indices that are selected from the `times` array. For example, if `step` is set to 2, every second index will be selected. If `step` is set to 3, every third index will be selected, and so. Defaults to 1
    """
    times = dbin.partial_get(idsname, "time")
    for timeVal in times[range(start, len(times) if stop is None else stop, step)]:
        dataSlice = dbin.get_slice(idsname, timeVal, imas.imasdef.PREVIOUS_INTERP)
        dbout.put_slice(dataSlice)


def resampleTimes(
    dbin: str,
    dbout: str,
    idsname: str,
    start: int = None,
    stop: int = None,
    step: int = None,
):
    """
    The function resampleTimes takes in a database input, database output, idsname, start, stop, and
    step parameters, and resamples the times in the input database based on the specified parameters,
    and puts the resampled data into the output database.

    Args:
        dbin (str): The parameter "dbin" is a string that represents the input database name. It is the database from which the data will be read.
        dbout (str): The parameter `dbout` is a string that represents the name of the output database. It is the database where the resampled data will be stored.
        idsname (str): The parameter "idsname" is a string that represents the ids that you want to resample.
        start (int): The start parameter is the index of the first time value to be resampled.
        stop (int): The `stop` parameter is used to specify the index at which the resampling should stop. If `stop` is not provided, the resampling will continue until the end of the `times` array.
        step (int): The `step` parameter determines the interval between the indices that are selected from the `times` array. For example, if `step` is set to 2, every second index will be selected. If `step` is set to 3, every third index will be selected, and so. Defaults to 1
    """
    times = dbin.partial_get(idsname, "time")
    if step is None:  # work on indices
        rstart = 0 if start is None else np.argmax(times >= start)
        rstop = len(times) if stop is None else (np.argmax(times > stop) - 1)
        rtimes = [times[range(rstart, rstop, 1)]]
    else:
        rstart = times[0] if start is None else start
        rstop = times[-1] if stop is None else stop
        rtimes = np.arange(rstart, rstop, step)

    for timeVal in rtimes:
        dataSlice = dbin.get_slice(idsname, timeVal, imas.imasdef.PREVIOUS_INTERP)
        dbout.put_slice(dataSlice)


def compareIds(X, Y, field=None, ignore_version=True, verb=True, output={}):
    """
    The function compares two ids objects and returns whether they are identical or not, along with a  dictionary of differences.

    Args:
        X: The first input ids object to compare.
        Y: The second input ids object to compare.
        field: The name of the field being compared in the IDSes.
        ignore_version: A boolean parameter that determines whether to ignore the "version_put" attribute when comparing the two objects. If set to True, the function will ignore this attribute. Defaults to True
        verb: a boolean indicating whether to print log messages during the comparison process. Defaults to True
        output: A dictionary that stores the output of the function, which includes information about any differences found between the two input objects.

    Returns:
        tuple containing a boolean value indicating whether the two input objects are identical, and a dictionary containing information about any differences found during the comparison.
    """

    identical = True
    if hasattr(X, "__name__") and hasattr(Y, "__name__"):
        if X.__name__ == Y.__name__:
            if field is None:
                field = X.__name__
                logger.debug("Has __name__ in IDSes :" + X.__name__)
        else:
            if verb:
                logger.error(f"Different IDSs: {X.__name__} and {Y.__name__}")
            return False
    elif hasattr(X, "_base_path") and hasattr(Y, "_base_path"):
        if X._base_path == Y._base_path:
            if field is None:
                field = X._base_path
                logger.debug("Has _base_path in IDSes :" + X._base_path)
        else:
            if verb:
                logger.error(f"Different structure: {X._base_path} and {Y._base_path}")
            return False
    else:
        # un-expected different objects
        logger.error(f"Unexpected objects: {type(X)} and {type(Y)}")
        return False

    Xd = X.__dict__
    Yd = Y.__dict__
    for key in set(Xd.keys()).union(set(Yd.keys())):
        if key.startswith("_"):
            continue

        if "hli_utils" == key:
            continue

        if ignore_version and "version_put" == key:
            continue

        if key not in Xd:
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    field + "." + key,
                    field + "." + key,
                    "not present in first ids",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.info(f"{key} not present in X")
            identical = False
            continue

        if key not in Yd:
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    field + "." + key,
                    field + "." + key,
                    "not present in second ids",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.info(f"{key} not present in Y")
            identical = False
            continue

        Xo = X.__dict__[key]
        Yo = Y.__dict__[key]
        if type(Xo) != type(Yo):
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    Xo,
                    Yo,
                    None,
                    f"different type first type(Xo), second type(Yo) ",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.warning(f"Different type for {field}.{key}")

        if hasattr(Xo, "__module__") and "imas" in Xo.__module__:
            # TO DO: To be removed, when private _base_path will be replaced by __name__
            if hasattr(Xo, "__name__"):
                attrname = Xo.__name__
            else:
                attrname = Xo._base_path
            identical_result, output = compareIds(
                Xo,
                Yo,
                field=f"{field}.{attrname}",
                ignore_version=ignore_version,
                verb=verb,
                output=output,
            )
            identical &= identical_result
            continue

        # treatment of struct_array and list of strings
        if type(Xo).__name__ == "list":
            data_type = list
            if len(Xo) != len(Yo):
                # avoids printing "array" as this is internal attribute for AoS
                if key == "array":
                    f = field
                else:
                    f = f"{field}.{key}"

                if f not in output.keys():
                    output[f] = (Xo, Yo, data_type, "different length")
                else:
                    logger.error("Duplicate key found")
                if verb:
                    logger.info(f"{f} is of different length")
                identical = False
            else:
                for i in range(len(Xo)):
                    if "structArrayElement" in type(Xo[i]).__name__:
                        identical_result, output = compareIds(
                            Xo[i],
                            Yo[i],
                            field=f"{field}[{i}]",
                            ignore_version=ignore_version,
                            verb=verb,
                            output=output,
                        )
                        identical &= identical_result
                    else:
                        # print("list of "+type(xo[i]).__name__)
                        continue
        else:
            # Check equalities of arrays first as numpy array
            if isinstance(Xo, np.ndarray) and isinstance(Yo, np.ndarray):
                result = np.array_equal(Xo, Yo, ARRAY_EQUAL_KWARGS)
                # output[field + "." + key]= (Xo, Yo, "equal")
            # and second as list
            else:
                result = Xo == Yo
                # output[field + "." + key]= (Xo, Yo, "equal")

            if not result:
                data_type = None
                missing = [False]
                if isinstance(Xo, np.ndarray):
                    data_type = np.ndarray
                    if Xo.size == 0:
                        missing = [True, "first"]
                    elif Yo.size == 0:
                        missing = [True, "second"]
                else:
                    missmap = {int: -999999999, float: -9e40}
                    for t in missmap:
                        if isinstance(Xo, t):
                            data_type = t
                            if Xo == missmap[t]:
                                missing = [True, "first"]
                            elif Yo == missmap[t]:
                                missing = [True, "second"]

                if missing[0]:
                    if field + "." + key not in output.keys():
                        output[field + "." + key] = (
                            Xo,
                            Yo,
                            data_type,
                            f"missing in the IDS {missing[1]}",
                        )
                    else:
                        logger.error("Duplicate key found")
                    if verb:
                        logger.info(f"{field}.{key} is missing in the {missing[1]} IDS")
                    identical = False
                else:
                    if field + "." + key not in output.keys():
                        output[field + "." + key] = (
                            Xo,
                            Yo,
                            data_type,
                            "different values",
                        )
                    else:
                        logger.error("Duplicate key found")
                    if verb:
                        logger.info(f"{field}.{key} has different values")
                    identical = False

    return identical, output


def getQuantitiesFromPulses(
    idspath: str, pulses: tuple, listCount: int = 0, verbose: bool = False
) -> pd.DataFrame:
    """
    The `getQuantitiesFromPulses` function retrieves values from a specified IDS path for a given set of pulses and returns a DataFrame containing the pulse, run, and corresponding values.

    Args:
        idspath (str): The `idspath` parameter is a string that represents the path to the IDS node from which the quantities will be extracted. It is used to specify the location of the data in the IDS
        pulses (tuple): The `pulses` parameter is a tuple containing information about each pulse. Each element in the tuple is itself a tuple with the following elements: pulse, run, backend, database, user, version, and file path.
        listCount (int): The `listCount` parameter is an optional parameter that specifies the number of pulses to retrieve values for. If `listCount` is set to 0 (default), values will be retrieved for all pulses in the `pulses` tuple. If `listCount` is set to a positive integer, values will be retrieved for first `listCount` pulses in the `pulses` tuple. Defaults to 0
        verbose (bool): print debug information

    Returns:
        The function `getQuantitiesFromPulses` returns a pandas DataFrame containing the columns "PULSE", "RUN", and "VALUE".
    """
    idsname = idspath.split("/")[0]
    valpath = idspath[1 + len(idsname) :]
    if listCount != 0:
        pulses = pulses[:listCount]
    values = []
    for pulseTuple in tqdm(pulses) if progbar else pulses:
        pulse = pulseTuple[0]
        run = pulseTuple[1]
        backend = pulseTuple[2]
        database = pulseTuple[3]
        user = pulseTuple[4]
        version = pulseTuple[5]
        if verbose:
            print(f"fetching data from {pulse}, {run}")
        connection = imas.DBEntry(backend, database, pulse, run, user, version)
        connection.open()
        try:
            values.append(connection.partial_get(idsname, valpath))
        except Exception:
            values.append(None)
        connection.close()

    df = pd.DataFrame(
        pulses,
        columns=[
            "PULSE",
            "RUN",
            "BACKEND",
            "DATABASE",
            "USER",
            "VERSION",
            "FILEPATH",
            "FILETIME",
        ],
    )
    df["VALUE"] = values
    dfExtract = df[["PULSE", "RUN", "VALUE"]]
    return dfExtract
