# TODO There are nonmigrated scripts that use the following functions, so
# keep this file. These functions are already migrated to
# utils/idshelper.py.
import imas
import inspect
import types


def is_field(idstype):
    """Checks if the passed type is possible field of an IDS.

    Parameters
    ----------
    idstype: type of an attribute from an IDS or a substructure of an IDS
    """
    return (
        idstype != types.method_type
        and idstype != types.function_type
        and "Logger" not in str(idstype)
        and "HLIUtils" not in str(idstype)
    )


def list_attributes(idsobj):
    """Returns a list of attributes names for the given IDS object.

    Parameters
    ----------
    idsobj: IDS or substructure object
    """
    if "imas" in str(type(idsobj)):
        return [a[0] for a in inspect.getmembers(idsobj) if not a[0].startswith("_") and is_field(type(a[1]))]
    else:
        return []


def all_ids_types():
    """Returns a list of strings corresponding to all IDS types defined in the version of IMAS being used."""
    return [ids.value for ids in list(imas.IDSName)]


def available_in_dbentry(db, time_mode=None):
    """Returns a list of pairs (idstype:str,occurrence:int) with data in the given DBEntry.

    Parameters
    ----------
    db: imas.DBEntry object
        an open DBEntry in which available IDSs will be looked for
    time_mode: int, optional
        time_mode of interest (imas.imasdef.IDS_TIME_MODE_HETEROGENEOUS, IDS_TIME_MODE_HOMOGENEOUS or
        IDS_TIME_MODE_INDEPENDENT)
        if not specified, occurrences of IDS in all time modes will be returned
    """
    presentidslist = []
    for idstype in all_ids_types():
        for occ in range(getattr(imas, idstype)().get_max_occurrences()):
            homogeneous_time = db.partial_get(idstype, "ids_properties/homogeneous_time", occurrence=occ)
            if homogeneous_time != imas.imasdef.EMPTY_INT and (time_mode is None or time_mode == homogeneous_time):
                presentidslist.append((idstype, occ))
    return presentidslist
