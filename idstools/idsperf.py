import cProfile
import sys
import timeit

try:
    import imaspy as imas
except ImportError:
    import imas


def get_ids(db, idsname, occ=0, times=None, interp=imas.ids_defs.PREVIOUS_INTERP, verbose=False, dd_update=False):
    """
    The function `get_ids` reads an IDS from a given DBEntry, either the entire IDS or slices at
    selected times, and returns the IDS object or a list of IDS slices.

    Args:
        db: The `db` parameter is an `imas.DBEntry` object, which represents an open data-entry for which the
            IDS will be read from. This object provides access to the data stored in the IMAS  database.
        idsname: The `idsname` parameter is a string that represents the name of the IDS that you want to read
            from the database.
        occ: The `occ` parameter is the occurrence number of the IDS to be read. It is an optional parameter
            and its default value is 0.
        times: A list of times at which to read a single slice of the IDS. If this parameter is not provided
            or set to None, the function will read the entire IDS.
        interp: The `interp` parameter is an optional parameter that specifies the slicing interpolation mode.
            It determines how the data is interpolated when reading a single slice at a specific time. The default
            value is `imas.ids_defs.PREVIOUS_INTERP`, which means that the data is interpolated using the previous
            time slice
        verbose: Verbose information

    Returns:
        either a full IDS object or a list of slices of an IDS object.
    """
    if times is None:
        if verbose:
            print(f"getting {idsname}")
        idsobj = db.get(idsname, occurrence=occ, autoconvert=False)
        if dd_update:
            idsobj = imas.convert_ids(idsobj, db.factory.version)
        if verbose:
            print(f"got {len(idsobj.time)} slices")
    else:
        idsobj = []
        for t in times:
            if verbose:
                print(f"getting a slice of {idsname} at time {t}")
            data_slice = db.get_slice(idsname, t, interp, occurrence=occ, autoconvert=False)
            if dd_update:
                data_slice = imas.convert_ids(data_slice, db.factory.version)
            idsobj.append(data_slice)
            if verbose:
                print(f"got {data_slice.time}")

    return idsobj


def get_timings(db, idsname, occ=0, dbout=None, times=None, repeat=5, verbose=False, profile=False, dd_update=False):
    """
    The function `get_timings` performs timing measurements for various I/O operations on an IDS in an IMAS database.

    Args:
        db: The `db` parameter is an `imas.DBEntry` object, which represents an open data-entry for which the IDS
            will be read from.
        idsname: The `idsname` parameter is a string that represents the name of the IDS to be read from the database.
        occ: The `occ` parameter is the occurrence number of the IDS to be read. It specifies which occurrence of
            the IDS to read from the database. By default, it is set to 0, which means the first occurrence.
            Defaults to 0
        dbout: The `dbout` parameter is an optional argument that specifies the output database where the
            IDS will be written to. If `dbout` is provided, the IDS will be written to the specified database.
        times: The `times` parameter is a list of times at which to read a single slice of the IDS. If `times`
            is set to `None`, the entire IDS will be read.
        repeat: The `repeat` parameter specifies the number of timings being measured. It allows for collecting
            statistics by repeating the timing measurement multiple times. Defaults to 5
        verbose: Verbose information
        profile: A boolean parameter that determines whether or not to print additional information by running
            the command under cProfile.

    Returns:
        The function `get_timings` returns a list of timing measurements. The length of the list is equal to the
        `repeat` parameter, which specifies the number of timings being measured. Each timing measurement represents
        the time taken to perform the specified I/O operation for the IDS.
    """
    if dbout is not None:
        if verbose:
            print("profiles put")
        idsobj = get_ids(db, idsname, occ, times, verbose, dd_update=dd_update)
        cmd = "dbout.put(idsobj)"
    else:
        cmd = f"get_ids(db,'{idsname}',occ=occ,times=times,verbose=verbose)"

    # Default timing
    # TODO: more fine grained control of imported symbols to avoid issues?
    t = timeit.Timer(cmd, globals={**locals(), **globals()})
    # 'from __main__ import get_ids,db,dbout,verbose,times,idsobj')
    timings = t.repeat(repeat=repeat, number=1)

    # Profiling
    if profile:
        cProfile.runctx(cmd, globals(), locals())

    return timings


def byte_size(obj):
    """Calculates recursively the approximated size of data of an IDS or its sub-structures.
    Does not take into account the overhead of the various containers.

    Parameters
    ----------
    obj: object (IDS or sub-structures)
        object from which data size is being measured

    Returns
    -------
    S: int
        estimated data size in bytes
    """
    s = 0
    for node in imas.util.tree_iter(obj):
        if isinstance(node, imas.ids_primitive.IDSString0D):
            s += len(node.value)
        elif isinstance(node, imas.ids_primitive.IDSNumericArray):
            s += node.value.nbytes
        elif isinstance(node, imas.ids_primitive.IDSInt0D):
            s += 4
        elif isinstance(node, imas.ids_primitive.IDSFloat0D):
            s += 8
        else:
            print(type(node), type(node.value), {sys.getsizeof(node.value)})
    return s
