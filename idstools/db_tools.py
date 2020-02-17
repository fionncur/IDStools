"""Library for retrieving IMAS database information.

@author H.-J. Klingshirn"""
from __future__ import print_function
import logging
import os
import sys

ALL_BACKENDS = "mdsplus", "hdf5"

def get_user_db_directory(user=None):
    """Get the IMAS database directory root for the user.
    If user is omitted, the current user is used."""
    if not user: user = os.getlogin()
    if (user=="public"):
        publichome = os.getenv("IMAS_HOME")
        if (publichome == None):
            print("Environment variable IMAS_HOME is not defined. Quitting.", file=sys.stderr)
            sys.exit(1)
        return publichome+'/shared/imasdb'
    else:
        return os.path.expanduser("~" + user + "/public/imasdb")

def list_tokamaks(user=None, dataversion=None):
    from os.path import join, isdir
    """List all tokamaks for a user.
    If user is omitted, current user is used.
    If dataversion is omitted, tokamaks for all dataversions are returned.

    Returns a list of tuples (tokamak, dataversions),
    where dataversions is a list of dataversion strings this tokamak exists for.
    """

    dbdir = get_user_db_directory(user)
    if not isdir(dbdir):
        return []

    dvs = dict()
    for tokamak in os.listdir(join(dbdir)):
        if not isdir(join(dbdir, tokamak)):
            continue

        tokDvs = list_dataversions_for_tokamak(tokamak, user)

        if dataversion and dataversion not in tokDvs:
                continue

        dvs[tokamak] = tokDvs

    return [ (tokamak, dvs[tokamak]) for tokamak in sorted(dvs.keys()) ]

def list_dataversions(user=None):
    """List dataversions existing for a given user.
    Returns a list of tuples (dataversion, tokamaks),
    where tokamaks is a list of tokamak names existing for every dataversion."""
    tokamakDvs = list_tokamaks(user=user)

    tokamaks = {}
    for tokamak, dvs in tokamakDvs:
        for dv in dvs:
            if dv not in tokamaks:
                tokamaks[dv] = []
            tokamaks[dv].append(tokamak)
    return [ (dv, tokamaks[dv]) for dv in sorted(tokamaks.keys())]

def list_dataversions_for_tokamak(tokamak, user=None):
    from os.path import join, isdir
    """List existing dataversions for a given tokamak.
    If user is omitted, current user is used.
    If dataversion is omitted, tokamaks for all dataversions are returned."""
    treedir = join(get_user_db_directory(user), tokamak)
    if not isdir(treedir):
        return []

    dvs = []
    for dv in os.listdir(treedir):
        if isdir(join(treedir, dv)):
            dvs.append(dv)
    return sorted(dvs)

def list_databases(user=None, tokamak=None, dataversion=None, backends=None):
    """List databases.
    If user is not given, the current user is used.
    If tokamak is given, only databases for the given tokamak are shown, otherwise databases for all tokamaks.
    If dataversion is given, only databases for the given database are shown, otherwise databases for all tokamaks.
    Argument backends is a list of backend names. If it's omitted, shots for all backends are returned.
    Note: the returned list of databases will only contain entries in the hierarchy
    for tokamaks, data versions and backends for which actual databases exist. To discover
    the full list of tokamaks, data versions and backends (even for combinations for which
    no actual databases are stored), use the methods list_dataversions_for_tokamak, list_tokamaks
    and list_backends.

    Returns a list of tuples (tokamakname, dataversion-list),
    where dataversion-list is a list of tuples (dataversion, backendlist),
    where backendlist is a list of tuples(backend, dblist),
    where dblist is a list of tuples (shotnum, runnums),
    where runnums is a list of integers.
    """

    result = []

    if not user: user = os.getlogin()
    if not backends:
        backends = ALL_BACKENDS

    if tokamak:
        tokamaks = [tokamak]
    else:
        tokamakDvs = list_tokamaks(user, dataversion)
        tokamaks = [ entry[0] for entry in tokamakDvs ]

    for tokamak in tokamaks:

        tokamakDbs = []
        if dataversion:
            dvs = [dataversion]
        else:
            dvs = list_dataversions_for_tokamak(tokamak, user)

        for dv in dvs:
            dvDbs = []
            for backend in backends:
                if backend == "mdsplus":
                    dbs = list_databases_mdsplus(user, tokamak, dv)
                elif backend == "hdf5":
                    dbs = list_databases_hdf5(user, tokamak, dv)
                else:
                    raise NotImplementedError("Unsupported backend: " + backend)
                if dbs:
                    dvDbs.append( (backend, dbs) )

            if dvDbs:
                tokamakDbs.append( (dv, dvDbs) )

        if tokamakDbs:
            result.append( (tokamak, tokamakDbs) )

    return result

def list_databases_mdsplus(user, tokamak, dataversion):
    """List all MDSPLUS databases for a given user, tokamak, dataversion."""
    from os.path import join, split, isdir
    import fnmatch

    mdsplusdir = join(get_user_db_directory(user), tokamak, dataversion)
    if not isdir(mdsplusdir):
        return []

    dbs = dict()
    for root, dirnames, filenames in os.walk(mdsplusdir):
        for filename in fnmatch.filter(filenames, '*.tree'):
            try:
                base, rundir = split(root)
                numStartPos = filename.find('_') + 1
                numEndPos = filename.rfind('.')
                num = int(filename[numStartPos:numEndPos])
                shot = int(num / 10000)
                run = int(rundir) * 10000 + (num % 10000)
                if shot not in dbs:
                    dbs[shot] = list()
                dbs[shot].append(run)
            except:
                 print("EXC: ", sys.exc_info(), file=sys.stderr)
                 logging.warn("Malformed MDSPlus database filename: " + join(root, filename))

    # create sorted lists
    return [ (shot, sorted(dbs[shot])) for shot in sorted(dbs.keys()) ]

def get_dbfiles_stem_mdsplus(user, tokamak, dataversion, shot, run):
    """Return the filename stem for the MDS+ database file with given parameters"""
    from os.path import join
    mdsplusdir = join(get_user_db_directory(user), tokamak, dataversion, "mdsplus")
    # filename is ids_<shot><run> where run is last four digits of run number,
    # right-aligned (filled with zeros).
    # Examples: 1
    run_string = str(run % 10000)
    if ( len(run_string) < 4 ):
        run_string = (4 - len(run_string)) * "0" + run_string
    stem = join(mdsplusdir, str(run / 10000), 'ids_' + str(shot) + run_string)
    return stem

def get_dbfiles_mdsplus(user, tokamak, dataversion, shot, run):
    """Return the MDS+ database filenames for a given IMAS database"""
    stem = get_dbfiles_stem_mdsplus(user, tokamak, dataversion, shot, run)
    return (stem + ".characteristics", stem + ".datafile", stem + ".tree")

def list_databases_hdf5(user, tokamak, dataversion):
    """List all HDF5 databases for a given user, tokamak, dataversion."""
    from os.path import join, split, isdir
    import fnmatch

    hdf5dir = join(get_user_db_directory(user), tokamak, dataversion)
    if not isdir(hdf5dir):
        return []

    dbs = dict()
    for root, dirnames, filenames in os.walk(hdf5dir):
        for filename in fnmatch.filter(filenames, '*.hd5'):
            try:
                parts = filename.replace(".hd5", "").split('_')
                shot = int(parts[1])
                run = int(parts[2])
                if shot not in dbs:
                    dbs[shot] = list()
                dbs[shot].append(run)
            except:
                logging.warn("Malformed HDF5 database filename: " + join(root, filename))

    # create sorted lists
    return [ (shot, sorted(dbs[shot])) for shot in sorted(dbs.keys()) ]

def get_dbfile_hdf5(user, tokamak, dataversion, shot, run):
    """Return the hdf5 database filename for a given IMAS database"""
    from os.path import join
    hdf5dir = join(get_user_db_directory(user), tokamak, dataversion, 'hdf5')
    return join(hdf5dir, 'ids_' + str(shot) + "_" + str(run) + ".hd5")

def get_dbfiles(user, tokamak, dataversion, shot, run, backend):
    """Return files storing this database."""
    if backend == "mdsplus":
        return get_dbfiles_mdsplus(user, tokamak, dataversion, shot, run)
    elif backend == "hdf5":
        return get_dbfile_hdf5(user, tokamak, dataversion, shot, run)
    else:
        raise NotImplementedError("Unsupported backend: " + backend)
