"""Library for retrieving IMAS database information.
#Original source idstools/db_tools.py
@author H.-J. Klingshirn"""
from __future__ import print_function
import logging
import os
import sys

ALL_BACKENDS = "mdsplus", "hdf5"


def getUserDatabaseDir(user=None) -> str:
    """
    This function returns the IMAS database directory root for a specified user or the current user.

    Args:
        user: An optional parameter that specifies the user for whom the IMAS database directory root is to be retrieved. If not provided, the current user is used.

    Returns:
        a string representing the IMAS database directory root for the specified user or the current user if no user is specified.
    """
    if not user:
        user = os.getlogin()
    if user != "public":
        return os.path.expanduser(f"~{user}/public/imasdb")
    imasHomeDir = os.getenv("IMAS_HOME")
    if imasHomeDir is None:
        print(
            "Environment variable IMAS_HOME is not defined. Quitting.",
            file=sys.stderr,
        )
        sys.exit(1)
    return f"{imasHomeDir}/shared/imasdb"


def getDatabases(user=None, version=None) -> list:
    # from os.path import join, isdir

    """List all tokamaks for a user.
    If user is omitted, current user is used.
    If dataversion is omitted, tokamaks for all dataversions are returned.

    Returns a list of tuples (tokamak, dataversions),
    where dataversions is a list of dataversion strings this tokamak exists for.
    """

    databaseDir = getUserDatabaseDir(user)
    if not os.path.isdir(databaseDir):
        return []

    databasesDict = {}
    for _database in os.listdir(os.path.join(databaseDir)):
        if not os.path.isdir(os.path.join(databaseDir, _database)):
            continue

        _databaseVersions = getDatabaseVersions(_database, user)

        if version and version not in _databaseVersions:
            continue

        databasesDict[_database] = _databaseVersions

    return [
        (database, databasesDict[database]) for database in sorted(databasesDict.keys())
    ]


def getDatabases2(user=None):
    """List dataversions existing for a given user.
    Returns a list of tuples (dataversion, tokamaks),
    where tokamaks is a list of tokamak names existing for every dataversion."""
    databaseWithVersionsDict = getDatabases(user=user)

    databaseDict = {}
    for database, versions in databaseWithVersionsDict:
        for _version in versions:
            if _version not in databaseDict:
                databaseDict[_version] = []
            databaseDict[_version].append(database)
    return [(version, databaseDict[version]) for version in sorted(databaseDict.keys())]


def getDatabaseVersions(databaseName, user=None):
    """
    This function returns a sorted list of all the versions of a given database located in a specific directory.

    Args:
        databaseName (str): A string representing the name of the database for which we want to retrieve the versions.
        user: The parameter "user" is an optional argument that can be passed to the function. It is used to specify the user for whom the database versions are to be retrieved. If no user is specified, the function will retrieve the database versions for the current user.

    Returns:
        The function `getDatabaseVersions` returns a sorted list of all the versions of a given database that exist in the user's database directory. If the database directory does not exist, an empty list is returned.
    """
    databaseDir = os.path.join(getUserDatabaseDir(user), databaseName)
    if not os.path.isdir(databaseDir):
        return []

    databaseVersions = [
        databaseVersion
        for databaseVersion in os.listdir(databaseDir)
        if os.path.isdir(os.path.join(databaseDir, databaseVersion))
    ]
    return sorted(databaseVersions)


def getDatabaseFiles(user=None, database=None, version=None, backends=None):
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

    if not user:
        user = os.getlogin()
    if not backends:
        backends = ALL_BACKENDS

    if database:
        databases = [database]
    else:
        _databases = getDatabases(user, version)
        databases = [entry[0] for entry in _databases]

    for database in databases:
        databaseFiles = []
        versions = [version] if version else getDatabaseVersions(database, user)
        for _version in versions:
            dvDbs = []
            for backend in backends:
                if backend == "hdf5":
                    dbs = list_databases_hdf5(user, database, _version)
                elif backend == "mdsplus":
                    dbs = list_databases_mdsplus(user, database, _version)
                else:
                    raise NotImplementedError(f"Unsupported backend: {backend}")
                if dbs:
                    dvDbs.append((backend, dbs))

            if dvDbs:
                databaseFiles.append((_version, dvDbs))

        if databaseFiles:
            result.append((database, databaseFiles))

    return result


def list_databases_mdsplus(user, tokamak, dataversion):
    """List all MDSPLUS databases for a given user, tokamak, dataversion."""
    from os.path import join, split, isdir, getmtime
    import fnmatch
    from datetime import datetime

    mdsplusdir = join(getUserDatabaseDir(user), tokamak, dataversion)
    if not isdir(mdsplusdir):
        return []

    dbs = dict()
    for root, dirnames, filenames in os.walk(mdsplusdir):
        for filename in fnmatch.filter(filenames, "*.tree"):
            try:
                base, rundir = split(root)
                numStartPos = filename.find("_") + 1
                numEndPos = filename.rfind(".")
                num = int(filename[numStartPos:numEndPos])
                shot = int(num / 10000)
                run = int(rundir) * 10000 + (num % 10000)
                if shot not in dbs:
                    dbs[shot] = list()
                dbs[shot].append(
                    (
                        run,
                        datetime.fromtimestamp(
                            getmtime(
                                get_dbfiles_mdsplus(
                                    user, tokamak, dataversion, shot, run
                                )[1]
                            )
                        ).replace(microsecond=0),
                    )
                )
            except:
                print("EXC: ", sys.exc_info(), file=sys.stderr)
                logging.warn(
                    "Malformed MDSPlus database filename: " + join(root, filename)
                )

    # create sorted lists
    return [(shot, sorted(dbs[shot])) for shot in sorted(dbs.keys())]


def get_dbfiles_stem_mdsplus(user, tokamak, dataversion, shot, run):
    """Return the filename stem for the MDS+ database file with given parameters"""
    from os.path import join

    mdsplusdir = join(getUserDatabaseDir(user), tokamak, dataversion)
    # filename is ids_<shot><run> where run is last four digits of run number,
    # right-aligned (filled with zeros).
    # Examples: 1
    run_string = str(run % 10000)
    if shot == 0:
        stem = join(mdsplusdir, str(int(run / 10000)), "ids_" + run_string.zfill(3))
    else:
        stem = join(
            mdsplusdir, str(int(run / 10000)), "ids_" + str(shot) + run_string.zfill(4)
        )
    return stem


def get_dbfiles_mdsplus(user, tokamak, dataversion, shot, run):
    """Return the MDS+ database filenames for a given IMAS database"""
    stem = get_dbfiles_stem_mdsplus(user, tokamak, dataversion, shot, run)
    return (stem + ".characteristics", stem + ".datafile", stem + ".tree")


def list_databases_hdf5(user, database, version):
    """List all HDF5 databases for a given user, tokamak, dataversion."""
    from os.path import join, split, isdir, getmtime
    import fnmatch
    from datetime import datetime

    hdf5dir = join(getUserDatabaseDir(user), database, version)
    if not isdir(hdf5dir):
        return []

    dbs = {}
    for root, dirnames, filenames in os.walk(hdf5dir):
        for filename in fnmatch.filter(filenames, "*.hd5"):
            try:
                parts = filename.replace(".hd5", "").split("_")
                shot = int(parts[1])
                run = int(parts[2])
                if shot not in dbs:
                    dbs[shot] = []
                dbs[shot].append(
                    (
                        run,
                        datetime.fromtimestamp(
                            getmtime(
                                get_dbfiles_hdf5(user, database, version, shot, run)[1]
                            )
                        ).replace(microsecond=0),
                    )
                )
            except Exception:
                logging.warn(
                    "Malformed HDF5 database filename: " + join(root, filename)
                )

    # create sorted lists
    return [(shot, sorted(dbs[shot])) for shot in sorted(dbs.keys())]


def get_dbfile_hdf5(user, tokamak, dataversion, shot, run):
    """Return the hdf5 database filename for a given IMAS database"""
    from os.path import join

    hdf5dir = join(getUserDatabaseDir(user), tokamak, dataversion, "hdf5")
    return join(hdf5dir, "ids_" + str(shot) + "_" + str(run) + ".hd5")


def get_dbfiles(user, tokamak, dataversion, shot, run, backend):
    """Return files storing this database."""
    if backend == "mdsplus":
        return get_dbfiles_mdsplus(user, tokamak, dataversion, shot, run)
    elif backend == "hdf5":
        return get_dbfile_hdf5(user, tokamak, dataversion, shot, run)
    else:
        raise NotImplementedError("Unsupported backend: " + backend)
