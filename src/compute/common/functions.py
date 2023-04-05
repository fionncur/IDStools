"""
This is a common module which has common functions which can be used across ll IDSes

"""
import logging
import numpy as np
from packaging import version
import csv

ARRAY_EQUAL_KWARGS = (
    "equal_nan=True" if version.parse(np.__version__) > version.parse("1.19") else ""
)
logger = logging.getLogger("module")


def nearest(array: np.ndarray, value: float) -> tuple:
    """
    Get index and nearest value from value asked from an array

    Args:
        array ([np.ndarray]): [numpy array]
        value ([float]): [value requested]

    Returns:
        [int]: [index found for value]
        [float]: [nearest value from value requested]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    index = abs(array - value).argmin()
    return index, array[index]


def middle(array: np.ndarray) -> tuple:
    """Get middle value from an array along with index

    Args:
        array (np.ndarray): [description]

    Returns:
        [type]: [description]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    length = len(array)
    index = int(length / 2)
    value = array[index]
    return index, value


def compare_ids(X, Y, field=None, ignore_version=True, verb=True, file_object=None):
    """
    Iterate over every field and compare values depending on the type of field.

    Parameters
    ----------
    X, Y: IDS like objects
          IDSs (or sub-structures) objects being compared
    field: str, optional
          name of the IDS (or sub-structure) being compared
    ignore_version: bool, optional
          ignore content of ids_properties.version_put for the comparison
    verb: bool, optional
          prints information about differences
    """
    writer = None
    if file_object is not None:
        writer = csv.writer(file_object)

    identical = True

    if hasattr(X, "__name__") and hasattr(Y, "__name__"):
        if X.__name__ == Y.__name__:
            if field is None:
                field = X.__name__
        else:
            if verb:
                logger.error(f"Different IDSs: {X.__name__} and {Y.__name__}")
            return False
    elif hasattr(X, "_base_path") and hasattr(Y, "_base_path"):
        if X._base_path == Y._base_path:
            if field is None:
                field = X._base_path
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
            if verb:
                logger.info(f"{key} not present in X")
            identical = False
            continue

        if key not in Yd:
            if verb:
                logger.info(f"{key} not present in Y")
            identical = False
            continue

        Xo = X.__dict__[key]
        Yo = Y.__dict__[key]
        if type(Xo) != type(Yo):
            if verb:
                logger.warning(f"Different type for {field}.{key}")

        if hasattr(Xo, "__module__") and "imas" in Xo.__module__:
            # TO DO: To be removed, when private _base_path will be replaced by __name__
            if hasattr(Xo, "__name__"):
                attrname = Xo.__name__
            else:
                attrname = Xo._base_path
            identical &= compare_ids(
                Xo,
                Yo,
                field=f"{field}.{attrname}",
                ignore_version=ignore_version,
                verb=verb,
                file_object=file_object,
            )
            continue

        # treatment of struct_array and list of strings
        if type(Xo).__name__ == "list":
            if len(Xo) != len(Yo):
                # avoids printing "array" as this is internal attribute for AoS
                if key == "array":
                    f = field
                else:
                    f = f"{field}.{key}"
                if verb:
                    if file_object is not None:
                        writer.writerow(["different length", f])
                        print("writer called")

                    logger.info(f"{f} is of different length")
                identical = False
            else:
                for i in range(len(Xo)):
                    if "structArrayElement" in type(Xo[i]).__name__:
                        identical &= compare_ids(
                            Xo[i],
                            Yo[i],
                            field=f"{field}[{i}]",
                            ignore_version=ignore_version,
                            verb=verb,
                            file_object=file_object,
                        )
                    else:
                        # print("list of "+type(xo[i]).__name__)
                        continue
        else:
            if isinstance(Xo, np.ndarray) and isinstance(Yo, np.ndarray):
                result = np.array_equal(Xo, Yo, ARRAY_EQUAL_KWARGS)
            else:
                result = Xo == Yo

            if not result:
                missing = [False]
                if isinstance(Xo, np.ndarray):
                    if Xo.size == 0:
                        missing = [True, "first"]
                    elif Yo.size == 0:
                        missing = [True, "second"]
                else:
                    missmap = {int: -999999999, float: -9e40}
                    for t in missmap:
                        if isinstance(Xo, t):
                            if Xo == missmap[t]:
                                missing = [True, "first"]
                            elif Yo == missmap[t]:
                                missing = [True, "second"]

                if missing[0]:
                    if verb:
                        if file_object is not None:
                            writer.writerow(["different values", field + "." + key])
                        logger.info(f"{field}.{key} is missing in the {missing[1]} IDS")
                    identical = False
                else:
                    if verb:
                        if file_object is not None:
                            writer.writerow(["different values", field + "." + key])
                        logger.info(f"{field}.{key} has different values")
                    identical = False

    return identical
