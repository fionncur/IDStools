import imas
import cProfile
import timeit


def get_ids(db,idsname,occ=0,times=None,interp=imas.imasdef.PREVIOUS_INTERP,verbose=False):
    """Function that reads an IDS from a given DBEntry, entirely or slices at selected times.

    Parameters
    ----------
    db: imas.DBEntry object
        the open data-entry for which the IDS will be read from
    idsname: str
        name of the IDS to be read
    occ: int, optional
        occurrence number of the IDS to be read
    times: list, optional 
        list of times at which to read a single slice (reads the entire IDS if times=None)
    interp: int, optional
        slicing interpolation mode
    verbose: bool, optional
        prints some information

    Returns
    -------
    idsobj: full IDS or list of slices of an IDS
    """
    if times is None:
        if verbose: print(f"getting {idsname}")
        idsobj = db.get(idsname,occurrence=occ)
        if verbose: print(f"got {len(idsobj.time)} slices")
    else:
        idsobj=[]
        for t in times:
            if verbose: print(f"getting a slice of {idsname} at time {t}")
            idsobj.append(db.get_slice(idsname,t,interp,occurrence=occ))
        if verbose: print(f"got {len(time)}")
        
    return idsobj;



def get_timings(db,idsname,occ=0,dbout=None,times=None,repeat=5,verbose=False,profile=False):
    """Function that performs the timing of various I/O operation for an IDS.

    Parameters
    ----------
    db: imas.DBEntry object
        the open data-entry for which the IDS will be read from
    idsname: str
        name of the IDS to be read
    occ: int, optional
        occurrence number of the IDS to be read
    times: list, optional 
        list of times at which to read a single slice (reads the entire IDS if times=None)
    repeat: int, optional
        number of timings being measured (to allow statistics)
    verbose: bool, optional
        prints some information
    profile: bool, optional
        prints even more information by running the command under cProfile

    Returns
    -------
    timings: list
        list of len==repeat of individual timing measurements 
    """
    
    if (dbout is not None):
        if verbose: print("profiles put")
        idsobj = get_ids(db,idsname,occ,times,verbose)
        cmd = "dbout.put(idsobj)"
    else:
        cmd = f"get_ids(db,'{idsname}',occ,times,verbose)"

    # Default timing
    # TODO: more fine grained control of imported symbols to avoid issues?
    t = timeit.Timer(cmd,globals={**locals(),**globals()})
    #'from __main__ import get_ids,db,dbout,verbose,times,idsobj')
    timings = t.repeat(repeat=repeat,number=1)

    # Profiling
    if profile:
        cProfile.run(cmd)

    return timings
    



