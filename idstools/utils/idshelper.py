"""
This module

"""

import inspect
import logging
import time
import types
import sys
import imaspy
import numpy as np
import pandas as pd
from packaging import version
from rich.progress import track

logger = logging.getLogger("module")
ARRAY_EQUAL_KWARGS = "equal_nan=True" if version.parse(np.__version__) > version.parse("1.19") else ""


def is_ids_field(idstype: type) -> bool:
    """
    This function checks if a given type is a possible field of an IDS.

    Args:
        idstype (type): The type of an attribute from an IDS or a substructure of an IDS.

    Returns:
        The function isIdsField returns a boolean value indicating whether the passed type is a possible
        field of an IDS or not.
    """
    return (
        idstype != types.MethodType
        and idstype != types.FunctionType
        and "Logger" not in str(idstype)
        and "HLIUtils" not in str(idstype)
    )


def get_ids_attributes(idsobj: object) -> list:
    """
    This function returns a list of attribute names for a given IDS object.

    Args:
        idsobj (object): The IDS or substructure object for which the function will return a list of attribute names.

    Returns:
        The function `get_ids_attributes` returns a list of attribute names for the given IDS object which are not
        private and are ids fields.
    """
    if "imas" in str(type(idsobj)):
        return [a[0] for a in inspect.getmembers(idsobj) if not a[0].startswith("_") and is_ids_field(type(a[1]))]
    else:
        return []


def get_ids_size(db_entry_object, ids_names=None) -> dict:
    """
    The function `get_ids_size` retrieves the size of IDS objects from a database entry and returns a dictionary
    containing the size in bytes and the time taken to read each object.

    Args:
        db_entry_object (): The `db_entry_object` parameter is an object of type ``. It
            is used to access the data in the IMAS database.
        ids_names: idsNames is a list of IDS names. If it is not provided, it defaults to None.

    Returns:
        a dictionary containing information about the size and time taken to read IDS objects from a database
        entry. The dictionary has the following structure:
    """
    
    if ids_names is None:
        factory = imaspy.IDSFactory()
        ids_names = factory.ids_names()
    if type(ids_names) is str:
        ids_names = ids_names.split(",")
    ids_size_dict = {}
    for ids_name in track(ids_names, description="[green]Processing..."):
        occurrence_list = db_entry_object.list_all_occurrences(ids_name)
        if len(occurrence_list) ==0:
            continue
        occurrences_count=max(occurrence_list)
        
        for o in range(occurrences_count + 1):
            ids_object = db_entry_object.get(
                    ids_name,  occurrence=o
                )
            homogeneous_time=ids_object.ids_properties.homogeneous_time
            if homogeneous_time >= 0:
                field = f"{ids_name}/{o}"
                ids_size_dict[field] = {}
                start_time = time.time()
                ids_size_dict[field]["time"] = time.time() - start_time
                ids_size_dict[field]["bytes"] = get_object_size(ids_object)
                print(
                    "Reading %0.3f MB of data for %s took %0.2f seconds"
                    % (
                        ids_size_dict[field]["bytes"] / 1024**2,
                        field,
                        ids_size_dict[field]["time"],
                    )
                )
                del ids_object
    return ids_size_dict


def get_all_ids_size(db_entry_object):
    """
    The function `get_all_ids_size` calculates the total size in bytes of all IDS in a given `db_entry_object`.

    Args:
        db_entry_object : The parameter `db_entry_object` is of type .

    Returns:
        the total size in bytes of all the IDS in the given `db_entry_object`.
    """
    ids_size_dict = get_ids_size(db_entry_object)
    total_bytes = np.array([ids["bytes"] for ids in ids_size_dict.values()]).sum()
    return total_bytes


def get_all_ids_get_time(db_entry_object):
    """
    The function `get_all_ids_get_time` calculates the total time for all IDS in a given `db_entry_object`.

    Args:
        db_entry_object : The parameter `db_entry_object` is of type .

    Returns:
        the total time to get all the IDSes in the given `db_entry_object`.
    """
    ids_size_dict = get_ids_size(db_entry_object)
    return np.array([ids["time"] for ids in ids_size_dict.values()]).sum()


def get_object_size(obj: object) -> int:
    object_size = 0
    
    if isinstance(obj, imaspy.ids_primitive.IDSInt0D)  or isinstance(obj, imaspy.ids_primitive.IDSString0D) or isinstance(obj, imaspy.ids_primitive.IDSComplex0D) or isinstance(obj, imaspy.ids_primitive.IDSFloat0D) or isinstance(obj, imaspy.ids_primitive.IDSNumericArray) or isinstance(obj, imaspy.ids_primitive.IDSPrimitive) or isinstance(obj, imaspy.ids_primitive.IDSString0D) or isinstance(obj, imaspy.ids_primitive.IDSString1D):
        if isinstance(obj.value, str):
            object_size += len(obj.value)
        elif isinstance(obj.value, np.ndarray):
            object_size += obj.value.nbytes
        elif isinstance(obj.value, int):
            object_size += 4
        elif isinstance(obj.value, float):
            object_size += 8
        elif isinstance(obj.value, list):
            for obj_item in obj:
                object_size += get_object_size(obj_item)
        else:
            print(f"Not implemented {type(obj.value)}  ->  {obj}" )
    elif isinstance(obj, imaspy.ids_struct_array.IDSStructArray):
        for obj_item in obj:
            object_size += get_object_size(obj_item)
    elif isinstance(obj, imaspy.ids_structure.IDSStructure):
        for obj_value in obj:
            object_size += get_object_size(obj_value)
    else:
        print(f"Not implemented {type(obj)}  ->  {obj}" )
    return object_size


def get_ids_types():
    """
    This function returns list of strings corresponding to all ids types for each IDSName object in the imas module.

    Returns:
        The function `get_ids_types()` is returning a list of values of all the `value` attributes of the `IDSName`
        objects in the `imas` module.
    """
    factory = imaspy.IDSFactory()
    return factory.ids_names()


def get_available_ids_and_occurrences(db_entry_object, time_mode=None, get_comment=False):
    """
    This function returns a list of pairs of available IDS types and their occurrences in a given DBEntry object.

    Args:
        db_entry_object (): An object of the class , which represents an open DBEntry in
            which available IDSs will be looked for.
        time_mode: The time mode of interest for the IDSs in the given DBEntry. It can be one of the following
        get_comment: Output ids_properties.comment field for each found occurrence

    Returns:
        a list of pairs (idstype:str,occurrence:int) with data in the given DBEntry.
    """
    occ_type_dict = {
        1: "reconstruction",
        2: "prediction_fixed",
        3: "prediction_free",
        4: "mapping",
    }
    availableidslist = []
    for idstype in get_ids_types():
        occurrence_list = db_entry_object.list_all_occurrences(idstype)
        if len(occurrence_list) ==0:
            continue
        max_occurrences=max(occurrence_list)
        for occ in range(max_occurrences + 1):
            homogeneous_time = ""
            comment = ""
            occ_type = ""
            ids_object = db_entry_object.get(
                    idstype,  occurrence=occ, lazy=True
                )
            homogeneous_time=ids_object.ids_properties.homogeneous_time
            comment = ids_object.ids_properties.homogeneous_time.comment
            try:
                occ_type_text = ""
                occ_type = ids_object.ids_properties.occurrence_type
                if occ_type.index != imaspy.ids_defs.EMPTY_INT:
                    occ_type_text = occ_type_dict[occ_type.index]
                    comment += f" [occurrence type = {occ_type_text}]"
            except Exception as e:
                logger.debug(f"{e}")
            if homogeneous_time != imaspy.ids_defs.EMPTY_INT and (time_mode is None or time_mode == homogeneous_time):
                if get_comment is True:
                    availableidslist.append((idstype, occ, comment))
                else:
                    availableidslist.append((idstype, occ))
    return availableidslist


def get_available_ids_and_times(db_entry_object) -> list:
    """
    The function `get_available_ids_and_times` retrieves available IDS names and corresponding time
    arrays from a given `db_entry_object`.

    Args:
        db_entry_object: The `db_entry_object` parameter.

    Returns:
        a list of tuples. Each tuple contains an IDS name and a corresponding time array.
    """

    result = []
    for _ids_name in get_ids_types():
        occurrence_list = db_entry_object.list_all_occurrences(_ids_name)
        if len(occurrence_list) ==0:
            continue
        max_occurrences=max(occurrence_list)

        for occurrence in range(max_occurrences + 1):
            time_array = None
            try:
                ids_object = db_entry_object.get(
                    _ids_name,  occurrence=occurrence, lazy=True
                )
                homogeneous_time=ids_object.ids_properties.homogeneous_time
                if homogeneous_time == imaspy.ids_defs.IDS_TIME_MODE_UNKNOWN:
                    time_array = []
                if homogeneous_time == imaspy.ids_defs.IDS_TIME_MODE_HETEROGENEOUS:
                    time_array = [np.NaN]
                if homogeneous_time == imaspy.ids_defs.IDS_TIME_MODE_HOMOGENEOUS:
                    time_array = db_entry_object.partial_get(_ids_name, "time")
                if homogeneous_time == imaspy.ids_defs.IDS_TIME_MODE_INDEPENDENT:
                    time_array = [np.NINF]
            except Exception as e:
                logger.debug(f"{e}")
                time_array = []
                logger.info(f"ERROR! IDS {_ids_name} : Reading time array fails due to following problem : {e}")
            if time_array is not None and len(time_array):
                result.append((_ids_name, time_array))
    return result


def resample_indices(dbin: str, dbout: str, idsname: str, start: int = 0, stop: int = None, step: int = 1):
    """
    The function resample_indices takes in a database input, database output, and an idsname, and resamples the
    data based on the specified start, stop, and step values.

    Args:
        dbin (str): The parameter "dbin" is a string that represents the input database name. It is the
            database from which the data will be read.
        dbout (str): The parameter `dbout` is a string that represents the name of the output database.
            It is the database where the resampled data will be stored.
        idsname (str): The parameter "idsname" is a string that represents the ids that you want to resample.
        start (int): The start parameter is the index of the first time value to be resampled.
        stop (int): The `stop` parameter is used to specify the index at which the resampling should stop.
            If `stop` is not provided, the resampling will continue until the end of the `times` array.
        step (int): The `step` parameter determines the interval between the indices that are selected from
            the `times` array. For example, if `step` is set to 2, every second index will be selected. If `step`
            is set to 3, every third index will be selected, and so. Defaults to 1
    """
    times = dbin.partial_get(idsname, "time")
    for time_val in times[range(start, len(times) if stop is None else stop, step)]:
        data_slice = dbin.get_slice(idsname, time_val, imaspy.ids_defs.PREVIOUS_INTERP)
        dbout.put_slice(data_slice)


def resample_times(
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
        dbin (str): The parameter "dbin" is a string that represents the input database name. It is the
            database from which the data will be read.
        dbout (str): The parameter `dbout` is a string that represents the name of the output database.
            It is the database where the resampled data will be stored.
        idsname (str): The parameter "idsname" is a string that represents the ids that you want to resample.
        start (int): The start parameter is the index of the first time value to be resampled.
        stop (int): The `stop` parameter is used to specify the index at which the resampling should stop.
            If `stop` is not provided, the resampling will continue until the end of the `times` array.
        step (int): The `step` parameter determines the interval between the indices that are selected from
            the `times` array. For example, if `step` is set to 2, every second index will be selected. If `step`
            is set to 3, every third index will be selected, and so. Defaults to 1
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

    for time_val in rtimes:
        data_slice = dbin.get_slice(idsname, time_val, imaspy.ids_defs.PREVIOUS_INTERP)
        dbout.put_slice(data_slice)


def compare_ids(
    x,
    y,
    field=None,
    ignore_version=True,
    verb=True,
    name_x="first",
    name_y="second",
    output={},
):
    """
    The function compares two ids objects and returns whether they are identical or not, along with a
    dictionary of differences.

    Args:
        x: The first input ids object to compare.
        y: The second input ids object to compare.
        field: The name of the field being compared in the IDSes.
        ignore_version: A boolean parameter that determines whether to ignore the "version_put" attribute when
            comparing the two objects. If set to True, the function will ignore this attribute. Defaults to True
        verb: a boolean indicating whether to print log messages during the comparison process. Defaults to True
        output: A dictionary that stores the output of the function, which includes information about any differences
            found between the two input objects.

    Returns:
        tuple containing a boolean value indicating whether the two input objects are identical, and a dictionary
        containing information about any differences found during the comparison.
    """

    identical = True
    if hasattr(x, "__name__") and hasattr(y, "__name__"):
        if x.__name__ == y.__name__:
            if field is None:
                field = x.__name__
                logger.debug("Has __name__ in IDSes :" + x.__name__)
        else:
            if verb:
                logger.error(f"Different IDSs: {x.__name__} and {y.__name__}")
            return False
    elif hasattr(x, "_base_path") and hasattr(y, "_base_path"):
        if x._base_path == y._base_path:
            if field is None:
                field = x._base_path
                logger.debug("Has _base_path in IDSes :" + x._base_path)
        else:
            if verb:
                logger.error(f"Different structure: {x._base_path} and {y._base_path}")
            return False
    else:
        # un-expected different objects
        logger.error(f"Unexpected objects: {type(x)} and {type(y)}")
        return False

    xd = x.__dict__
    yd = y.__dict__
    for key in set(xd.keys()).union(set(yd.keys())):
        if key.startswith("_"):
            continue

        if "hli_utils" == key:
            continue

        if ignore_version and "version_put" == key:
            continue

        if key not in xd:
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    field + "." + key,
                    field + "." + key,
                    f"not present in {name_x} ids",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.info(f"{key} not present in X")
            identical = False
            continue

        if key not in yd:
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    field + "." + key,
                    field + "." + key,
                    f"not present in {name_y} ids",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.info(f"{key} not present in Y")
            identical = False
            continue

        xo = x.__dict__[key]
        yo = y.__dict__[key]
        if not isinstance(xo, type(yo)):
            if field + "." + key not in output.keys():
                output[field + "." + key] = (
                    xo,
                    yo,
                    None,
                    f"different type {name_x} type(Xo), {name_y} type(Yo) ",
                )
            else:
                logger.error("Duplicate key found")
            if verb:
                logger.warning(f"Different type for {field}.{key}")

        if hasattr(xo, "__module__") and "imas" in xo.__module__:
            # TO DO: To be removed, when private _base_path will be replaced by __name__
            if hasattr(xo, "__name__"):
                attrname = xo.__name__
            else:
                attrname = xo._base_path
            identical_result, output = compare_ids(
                xo,
                yo,
                field=f"{field}.{attrname}",
                ignore_version=ignore_version,
                verb=verb,
                name_x=name_x,
                name_y=name_y,
                output=output,
            )
            identical &= identical_result
            continue

        # treatment of struct_array and list of strings
        if type(xo).__name__ == "list":
            data_type = list
            if len(xo) != len(yo):
                # avoids printing "array" as this is internal attribute for AoS
                if key == "array":
                    f = field
                else:
                    f = f"{field}.{key}"

                if f not in output.keys():
                    output[f] = (xo, yo, data_type, "different length")
                else:
                    logger.error("Duplicate key found")
                if verb:
                    logger.info(f"{f} is of different length")
                identical = False
            else:
                for i in range(len(xo)):
                    if "structArrayElement" in type(xo[i]).__name__:
                        identical_result, output = compare_ids(
                            xo[i],
                            yo[i],
                            field=f"{field}[{i}]",
                            ignore_version=ignore_version,
                            verb=verb,
                            name_x=name_x,
                            name_y=name_y,
                            output=output,
                        )
                        identical &= identical_result
                    else:
                        # print("list of "+type(xo[i]).__name__)
                        continue
        else:
            # Check equalities of arrays first as numpy array
            if isinstance(xo, np.ndarray) and isinstance(yo, np.ndarray):
                result = np.array_equal(xo, yo, ARRAY_EQUAL_KWARGS)
                # output[field + "." + key]= (Xo, Yo, "equal")
            # and second as list
            else:
                result = xo == yo
                # output[field + "." + key]= (Xo, Yo, "equal")

            if not result:
                data_type = None
                missing = [False]
                if isinstance(xo, np.ndarray):
                    data_type = np.ndarray
                    if xo.size == 0:
                        missing = [True, name_x]
                    elif yo.size == 0:
                        missing = [True, name_y]
                else:
                    missmap = {int: -999999999, float: -9e40}
                    for t in missmap:
                        if isinstance(xo, t):
                            data_type = t
                            if xo == missmap[t]:
                                missing = [True, name_x]
                            elif yo == missmap[t]:
                                missing = [True, name_y]

                if missing[0]:
                    if field + "." + key not in output.keys():
                        output[field + "." + key] = (
                            xo,
                            yo,
                            data_type,
                            f"missing in {missing[1]}",
                        )
                    else:
                        logger.error("Duplicate key found")
                    if verb:
                        logger.info(f"{field}.{key} is missing in {missing[1]}")
                    identical = False
                else:
                    if field + "." + key not in output.keys():
                        output[field + "." + key] = (
                            xo,
                            yo,
                            data_type,
                            "different values",
                        )
                    else:
                        logger.error("Duplicate key found")
                    if verb:
                        logger.info(f"{field}.{key} has different values")
                    identical = False

    return identical, output


def get_quantities_from_pulses(idspath: str, pulses: tuple, list_count: int = 0, verbose: bool = False) -> pd.DataFrame:
    """
    The `get_quantities_from_pulses` function retrieves values from a specified IDS path for a given set of pulses and
    returns a DataFrame containing the pulse, run, and corresponding values.

    Args:
        idspath (str): The `idspath` parameter is a string that represents the path to the IDS node from which the
            quantities will be extracted. It is used to specify the location of the data in the IDS
        pulses (tuple): The `pulses` parameter is a tuple containing information about each pulse. Each element in
            the tuple is itself a tuple with the following elements: pulse, run, backend, database, user, version, and
            file path.
        list_count (int): The `list_count` parameter is an optional parameter that specifies the number of pulses to
            retrieve values for. If `list_count` is set to 0 (default), values will be retrieved for all pulses in the
            `pulses` tuple. If `list_count` is set to a positive integer, values will be retrieved for first `listCount`
            pulses in the `pulses` tuple. Defaults to 0
        verbose (bool): print debug information

    Returns:
        The function `get_quantities_from_pulses` returns a pandas DataFrame containing the columns "PULSE", "RUN",
        and "VALUE".
    """
    idsname = idspath.split("/")[0]
    valpath = idspath[1 + len(idsname) :]
    if list_count != 0:
        pulses = pulses[:list_count]
    values = []
    for pulse_tuple in track(pulses, description="[green]Processing..."):
        pulse = pulse_tuple[0]
        run = pulse_tuple[1]
        backend = pulse_tuple[2]
        database = pulse_tuple[3]
        user = pulse_tuple[4]
        version = pulse_tuple[5]
        if verbose:
            print(f"fetching data from {pulse}, {run}")
        connection = (backend, database, pulse, run, user, version)
        connection.open()
        try:
            values.append(connection.partial_get(idsname, valpath))
        except Exception as e:
            logger.debug(f"{e}")
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
    df_extract = df[["PULSE", "RUN", "VALUE"]]
    return df_extract


# if __name__ == "__main__":
#     import imaspy
#     entry = imaspy.DBEntry("imas:mdsplus?user=public;shot=131024;run=41;database=ITER;version=3", "r")  

#     # Open the database entry, providing legacy Data Entry parameters
#     imas_entry = imaspy.DBEntry(imaspy.ids_defs.MDSPLUS_BACKEND, "ITER", 131024, 41, "public")
#     imas_entry.open()
#     core_profiles = imas_entry.get("core_profiles", lazy=False)

#     print(core_profiles.ids_properties)

#     # print(get_ids_attributes(core_profiles))
#     print(get_ids_size(entry, ["summary"]))