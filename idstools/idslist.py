import imas


def all_ids_types():
    """Returns a list of strings corresponding to all IDS types defined in the version of IMAS being used.
    """
    return [ids.value for ids in list(imas.IDSName)]


def available_in_dbentry(db, time_mode=None):
    """Returns a list of pairs (idstype:str,occurrence:int) with data in the given DBEntry.

    Parameters
    ----------
    db: imas.DBEntry object
        an open DBEntry in which available IDSs will be looked for 
    time_mode: int, optional
        time_mode of interest (imas.imasdef.IDS_TIME_MODE_HETEROGENEOUS, IDS_TIME_MODE_HOMOGENEOUS or IDS_TIME_MODE_INDEPENDENT)
        if not specified, occurrences of IDS in all time modes will be returned
    """
    presentidslist = []
    for idstype in all_ids_types():
        for occ in range(getattr(imas,idstype)().getMaxOccurrences()):
            homogeneous_time = db.partial_get(idstype,"ids_properties/homogeneous_time",occurrence=occ)
            if homogeneous_time!=imas.imasdef.EMPTY_INT and (time_mode==None or time_mode==homogeneous_time):
                presentidslist.append((idstype,occ))
    return presentidslist
