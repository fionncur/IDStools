"""
This module 

"""
import inspect
import logging
import types

import imas
import numpy as np
from packaging import version

logger = logging.getLogger("module")
ARRAY_EQUAL_KWARGS = (
    "equal_nan=True" if version.parse(np.__version__) > version.parse("1.19") else ""
)


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
    presentidslist = []
    for idstype in getIdsTypes():
        for occ in range(getattr(imas, idstype)().getMaxOccurrences()):
            homogeneous_time = dbEntryObject.partial_get(
                idstype, "ids_properties/homogeneous_time", occurrence=occ
            )
            if homogeneous_time != imas.imasdef.EMPTY_INT and (
                time_mode is None or time_mode == homogeneous_time
            ):
                presentidslist.append((idstype, occ))
    return presentidslist


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
