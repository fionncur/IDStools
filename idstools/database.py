import fnmatch
import logging
import os

from datetime import datetime
from glob import glob
from pathlib import Path
from idstools.utils.clihelper import getBackendID

import imas
import yaml


logger = logging.getLogger(f"module.{__name__}")


class DBMaster:
    ALL_BACKENDS = "mdsplus", "hdf5"

    @staticmethod
    def getUserDir(user: str = None):
        """
        The function `getUserDir` returns the database directory path for a given user or the current user's directory path if no user is specified.

        Args:
            user (str): The `user` parameter is a string that represents the username of the user for whom the directory path is being retrieved. If the `user` parameter is not provided or is `None`, it will default to the current logged-in user obtained using `os.getlogin()`.

        Returns:
            a file path. If the user is not specified or is "public", it returns the file path to the "public/imasdb/" directory in the user's home directory. If the user is not "public", it returns the file path to the "shared/imasdb/" directory in the IMAS_HOME directory.
        """
        if not user:
            user = os.getlogin()
        if user != "public":
            return f'{os.path.expanduser(f"~{user}")}/public/imasdb/'
        imasHomeDir = os.environ["IMAS_HOME"]
        if imasHomeDir is None:
            raise FileNotFoundError(
                "File path in the environment variable IMAS_HOME is not defined."
            )
        return f"{imasHomeDir}/shared/imasdb/"

    @staticmethod
    def getDatabaseDir(database: str, user: str = None):
        """
        The function `getDatabaseDir` returns the directory path for a given database, and raises an error if the path does not exist.

        Args:
            database (str): The `database` parameter is a string that represents the name of the database file or directory.
            user (str): The `user` parameter is an optional parameter that represents the user for whom the database directory is being retrieved.

        Returns:
            the directory path of the specified database if it exists. If the database does not exist, it raises a FileNotFoundError. If the database parameter is None, it returns None.
        """
        userDir = DBMaster.getUserDir(user)

        if database is not None:
            userDatabaseDir = userDir + database
            if os.path.exists(userDatabaseDir):
                return userDatabaseDir
            else:
                raise FileNotFoundError(
                    "The path provided does not exist or has no such database file or directory. Please check spelling."
                )
        return None

    @staticmethod
    def getVersionDir(version: str, database: str, user: str = None):
        """
        The function `getVersionDir` returns the directory path for a specific version of a database, given the version, database name, and optional user.

        Args:
            version (str): The version parameter is a string that represents the version of the database.
            database (str): The `database` parameter is a string that represents the name of the database.
            user (str): The `user` parameter is an optional parameter

        Returns:
            the directory path for the specified version of a database. If the version directory exists, it returns the path. If the version directory does not exist, it raises a FileNotFoundError. If the version parameter is None, it returns None.
        """
        databaseDir = DBMaster.getDatabaseDir(database, user)
        if version is not None:
            versionDir = f"{databaseDir}/{version}"
            if os.path.exists(versionDir):
                return versionDir
            else:
                raise FileNotFoundError(
                    "The path provided does not exist or has no such database file or directory. Please check spelling."
                )
        return None

    @staticmethod
    def getDatabases(user: str = None) -> list:
        """
        The function `getDatabases` returns a sorted list of databases in a user's directory.

        Args:
            user (str): The `user` parameter is a string that represents the username of the user for whom the databases are being retrieved.

        Returns:
            a list of databases.
        """
        userDir = DBMaster.getUserDir(user)
        databases = [
            _database
            for _database in os.listdir(userDir)
            if os.path.isdir(os.path.join(userDir, _database))
        ]
        return sorted(databases)

    @staticmethod
    def getVersions(database: str, user: str = None) -> list:
        """
        The function `getVersions` returns a sorted list of versions in a given database directory.

        Args:
            database (str): A string representing the name of the database.
            user (str): The `user` parameter is an optional parameter

        Returns:
            a sorted list of versions.
        """
        databaseDir = DBMaster.getDatabaseDir(database, user)
        versions = [
            _version
            for _version in os.listdir(databaseDir)
            if os.path.isdir(os.path.join(databaseDir, _version))
        ]
        return sorted(versions)

    @staticmethod
    def getDatabasesWithVersions(user: str = None) -> list:
        """
        The function `getDatabasesWithVersions` returns a list of tuples, where each tuple contains the  name of a database and a list of its versions, for a given user.

        Args:
            user (str): The `user` parameter is a string that represents the username or identifier of the  user for whom the databases and their versions are being retrieved. It is an optional parameter and can be set to `None` if not applicable.

        Returns:
            a list of tuples. Each tuple contains the name of a database and a list of versions associated  with that database. The list is sorted by the database names.
        """
        userDir = DBMaster.getUserDir(user)
        databasesDict = {}
        for _database in os.listdir(userDir):
            if not os.path.isdir(os.path.join(userDir, _database)):
                continue
            _databaseVersions = DBMaster.getVersions(_database, user)
            databasesDict[_database] = _databaseVersions
        return [
            (database, databasesDict[database])
            for database in sorted(databasesDict.keys())
        ]

    @staticmethod
    def getVersionsWithDatabases(user: str = None) -> list:
        """
        The function `getVersionsWithDatabases` returns a list of tuples, where each tuple contains a version number and a list of databases associated with that version.

        Args:
            user (str): The `user` parameter is an optional string
        Returns:
            a list of tuples. Each tuple contains a version number and a list of databases that have that version. The list is sorted in ascending order based on the version numbers.
        """
        databaseWithVersionsDict = DBMaster.getDatabasesWithVersions(user=user)

        databaseDict = {}
        for database, versions in databaseWithVersionsDict:
            for _version in versions:
                if _version not in databaseDict:
                    databaseDict[_version] = []
                databaseDict[_version].append(database)
        return [
            (version, databaseDict[version]) for version in sorted(databaseDict.keys())
        ]

    @staticmethod
    def getHdf5Pulses(
        user: str = None, database: str = None, version: str = None, asDictionary=False
    ) -> list:
        """
        The function `getHdf5Pulses` retrieves a list of pulses from HDF5 master files. It needs to specify full path till version.

        Returns:
            a list of tuples. Each tuple contains the following elements, The tuple includes the pulse number, run number, HDF5_BACKEND backend, database, user, version, and data file path.
        """
        versionDir = DBMaster.getVersionDir(version, database, user)
        pulses = {} if asDictionary else []
        hdf5MasterFilePaths = glob(f"{versionDir}/**/*master.h5", recursive=True)
        for hdf5MasterFilePath in hdf5MasterFilePaths:
            try:
                pulse = int(str(hdf5MasterFilePath).split("/")[-3])
                run = int(str(hdf5MasterFilePath).split("/")[-2])
            except:
                print(f"Malformed database path {hdf5MasterFilePath}")
                continue
            fileTime = datetime.fromtimestamp(
                os.path.getmtime(hdf5MasterFilePath)
            ).replace(microsecond=0)

            if asDictionary:
                if pulse not in pulses:
                    pulses[pulse] = []
                pulses[pulse].append(
                    (
                        pulse,
                        run,
                        imas.imasdef.MDSPLUS_BACKEND,
                        database,
                        user,
                        version,
                        hdf5MasterFilePath,
                        fileTime,
                    )
                )
            else:
                pulses.append(
                    (
                        pulse,
                        run,
                        imas.imasdef.HDF5_BACKEND,
                        database,
                        user,
                        version,
                        hdf5MasterFilePath,
                        fileTime,
                    )
                )
        return pulses

    @staticmethod
    def getMdsPlusPulses(
        user: str = None,
        database: str = None,
        version: str = None,
        status: str = None,
        asDictionary=False,
    ) -> list:
        """
        The function `getMdsPlusPulses` retrieves a list of MDSPlus pulses based on the provided user, database, version, and status parameters.

        Args:
            user (str): The `user` parameter is a string that represents the user for whom the MDSPlus
        pulses are being retrieved.
            database (str): The `database` parameter is a string that represents the name of the database. It is used to specify the directory where the MDSplus pulses are stored.
            version (str): The `version` parameter is used to specify the version of the MDSplus database. It is a string that represents the version number.
            status (str): The "status" parameter is used to filter the pulses based on their status. If a status is provided, only pulses with that status will be included in the result. If no status is provided, all pulses will be included.
            asDictionary (bool): The `asDictionary` parameter is a boolean flag that determines the format of the returned pulses. If `asDictionary` is set to `True`, the pulses will be returned as a dictionary where the keys are the pulse numbers and the values are lists of runs associated with each pulse. If `as. Defaults to False

        Returns:
            a list of pulses.
        """
        mdsplusDir = DBMaster.getVersionDir(version, database, user)
        pulses = {} if asDictionary else []

        for root, dirnames, filenames in os.walk(mdsplusDir):
            for datafile in fnmatch.filter(filenames, "*.datafile"):
                dataFilePath = f"{root}/{datafile}"
                if (status is None) or (
                    status
                    == DBMaster.getPulseStatus(Path(dataFilePath).with_suffix(".yaml"))
                ):
                    runList = (root[len(mdsplusDir) + 1 :]).split("/")
                    try:
                        if len(runList) == 1:  # AL4 layout
                            numStartPos = datafile.find("_") + 1
                            numEndPos = datafile.rfind(".")
                            num = int(datafile[numStartPos:numEndPos])
                            pulse = num // 10000
                            run = int(runList[0]) * 10000 + (num % 10000)
                        else:  # AL5 layout
                            assert datafile == "ids_001.datafile"
                            if os.path.islink(dataFilePath):
                                continue
                            run = root.split("/")[-1]
                            run = int(run)
                            pulse = root.split("/")[-2]
                            pulse = int(pulse)
                    except:
                        print(f"Malformed database path {root}")
                        continue
                    fileTime = datetime.fromtimestamp(
                        os.path.getmtime(dataFilePath)
                    ).replace(microsecond=0)

                    if asDictionary:
                        if pulse not in pulses:
                            pulses[pulse] = []
                        isRunAvailable = any(x[1] == run for x in pulses[pulse])
                        if not isRunAvailable:
                            pulses[pulse].append(
                                (
                                    pulse,
                                    run,
                                    imas.imasdef.MDSPLUS_BACKEND,
                                    database,
                                    user,
                                    version,
                                    dataFilePath,
                                    fileTime,
                                )
                            )
                    else:
                        pulses.append(
                            (
                                pulse,
                                run,
                                imas.imasdef.MDSPLUS_BACKEND,
                                database,
                                user,
                                version,
                                dataFilePath,
                                fileTime,
                            )
                        )
        return pulses

    @staticmethod
    def getPulseStatus(yamlFilePath: str) -> str:
        """
        The function `getPulseStatus` reads a YAML file from a given path and returns the value of the
        "status" key in the file's metadata.

        Args:
            path: The `path` parameter is a string that represents the file path to a YAML file.

        Returns:
            the value of the "status" key from the metadata dictionary.
        """
        _yamlFilePath = Path(yamlFilePath)
        try:
            with open(_yamlFilePath, "r") as fileHandle:
                metadata = yaml.safe_load(fileHandle)
        except FileNotFoundError as exc:
            print(exc)
            return "unknown"
        return metadata["status"]

    @staticmethod
    def getDatabaseFiles(user=None, database=None, version=None, backends=None):
        """
        The function `getDatabaseFiles` retrieves a list of database files based on the specified user,  database, version, and backends.

        Args:
            user: The `user` parameter is used to specify the user for whom the database files are being retrieved. If no user is specified, it defaults to `None`.
            database: The `database` parameter is used to specify the name of the database.
            version: The `version` parameter is used to specify a specific version of the database.
            backends: The `backends` parameter is a list of strings that specifies the database backends to retrieve files from. The possible values for `backends` are "hdf5" and "mdsplus". If `backends` is not provided, it defaults to `DBMaster.ALL_BACKENDS

        Returns:
            The function `getDatabaseFiles` returns a list of tuples. Each tuple contains the name of a database, followed by a list of tuples. Each inner tuple contains a version number, followed by a list of tuples. Each innermost tuple contains the name of a backend (either "hdf5" or "mdsplus"), followed by a dictionary of database files.
        """
        result = []

        if not backends:
            backends = DBMaster.ALL_BACKENDS

        databases = [database] if database else DBMaster.getDatabases(user)
        for database in databases:
            databaseFiles = []
            versions = [version] if version else DBMaster.getVersions(database, user)
            for _version in versions:
                pulses = []
                for backend in backends:
                    if backend == "hdf5":
                        dbs = DBMaster.getHdf5Pulses(
                            user, database, _version, asDictionary=True
                        )
                    elif backend == "mdsplus":
                        dbs = DBMaster.getMdsPlusPulses(
                            user, database, _version, asDictionary=True
                        )
                    else:
                        raise NotImplementedError(f"Unsupported backend: {backend}")
                    if dbs:
                        pulses.append((backend, dbs))
                if pulses:
                    databaseFiles.append((_version, pulses))
            if databaseFiles:
                result.append((database, databaseFiles))
        return result

    @staticmethod
    def getHDF5PhysicalFile(user, database, version, pulse, run):
        """
        The function `getHDF5PhysicalFile` returns the path to an HDF5 file based on the user, database, version, pulse, and run.

        Args:
            user: The "user" parameter represents the name of the user who is accessing the HDF5 physical file.
            database: The "database" parameter refers to the name of the database where the HDF5 files are stored.
            version: The "version" parameter represents the version of the database.
            pulse: The "pulse" parameter represents the pulse number. It is a numerical value that identifies a specific pulse in a dataset.
            run: The "run" parameter represents the run number.

        Returns:
            the path to an HDF5 physical file.
        """
        hdf5dir = os.path.join(DBMaster.getUserDir(user), database, version, "hdf5")
        return os.path.join(hdf5dir, f"ids_{str(pulse)}_{str(run)}.hd5")

    @staticmethod
    def getMDSPlusPhysicalFiles(user, database, version, pulse, run):
        """
        The function `getMDSPlusPhysicalFiles` returns the MDS+ database filenames for a given IMAS
        database.

        Args:
            user: The "user" parameter is the username of the user accessing the IMAS database.
            database: The `database` parameter refers to the name of the IMAS database.
            version: The "version" parameter represents the version of the IMAS database.
            pulse: The parameter "pulse" represents the pulse number in the IMAS database.
            run: The "run" parameter is the run number.

        Returns:
            The function `getMDSPlusPhysicalFiles` returns a tuple of three strings. The first string is the filename with the extension ".characteristics", the second string is the filename with the extension ".datafile", and the third string is the filename with the extension ".tree".
        """
        mdsplusdir = os.path.join(DBMaster.getUserDir(user), database, version)
        # filename is ids_<shot><run> where run is last four digits of run number,
        # right-aligned (filled with zeros).
        # Examples: 1
        run_string = str(run % 10000)
        if pulse == 0:
            mdsplusFileName = os.path.join(
                mdsplusdir, str(int(run / 10000)), f"ids_{run_string.zfill(3)}"
            )
        else:
            mdsplusFileName = os.path.join(
                mdsplusdir,
                str(int(run / 10000)),
                f"ids_{str(pulse)}{run_string.zfill(4)}",
            )
        return (
            f"{mdsplusFileName}.characteristics",
            f"{mdsplusFileName}.datafile",
            f"{mdsplusFileName}.tree",
        )

    @staticmethod
    def getPhysicalFiles(user, database, version, pulse, run, backend):
        """
        The function `getPhysicalFiles` returns the physical files storing a database based on the
        specified backend.

        Args:
            user: The user parameter represents the user who is requesting the physical files.
            database: The "database" parameter refers to the name or identifier of the database for which you want to retrieve the physical files.
            version: The version parameter represents the version of the database. It is used to retrieve the physical files associated with a specific version of the database.
            pulse: The "pulse" parameter refers to a specific pulse or shot number in a database. It is used to identify a particular data acquisition event or experiment.
            run: The "run" parameter is used to specify the run number or identifier for the database. It is likely used to retrieve the physical files associated with a specific run of the database.
            backend: The "backend" parameter refers to the type of database backend being used. It can have two possible values: "mdsplus" or "hdf5".

        Returns:
            The function `getPhysicalFiles` returns the physical file path storing the specified database.
        """
        """Return files storing this database."""
        if backend == "mdsplus":
            return DBMaster.getMDSPlusPhysicalFiles(user, database, version, pulse, run)
        elif backend == "hdf5":
            return DBMaster.getHDF5PhysicalFile(user, database, version, pulse, run)
        else:
            raise NotImplementedError(f"Unsupported backend: {backend}")

    @classmethod
    def getIMASVersion(cls):
        lowlevelVersion=int((os.getenv("AL_VERSION") or os.getenv("UAL_VERSION"))[0])
        return lowlevelVersion

    @classmethod
    def getConnection(cls, args):
        
        imasVersion = DBMaster.getIMASVersion()
        if imasVersion > 4:
            if args.uri is None:
                if args.pulse is None or args.run is None:
                    logger.error("Both the path or the shot/pulse and run are missing.")
                    return None
                connection = imas.DBEntry(
                    getBackendID(args.backend),
                    args.database,
                    args.pulse,
                    args.run,
                    args.user,
                )
            else:
                if args.pulse is not None and args.run is not None:
                    logger.warning(
                        "Both uri and legacy parameters are provided. Using path for accessing data entry"
                    )
                if "mode" in args.__dict__:
                    connection = imas.DBEntry(args.uri, args.mode)
                else:
                    connection = imas.DBEntry(args.uri, "r")
                    
        else:
            if args.shot is None or args.run is None:
                logger.error("There is no shot and run available")
                return None
            connection = imas.DBEntry(
                getBackendID(args.backend),
                args.database,
                args.shot,
                args.run,
                args.user,
            )
        status, _ = connection.open()
        if status != 0:
            logger.error(f"The specified database is not available")
            return None
        return connection


def readScenario(
    scenarioFilePath: str,
    inIDSList: list = None,
    outIDSList: list = None,
    testMode: bool = False,
    **testArgs,
):
    """
    This function reads a scenario file and takes in optional input and output IDs lists, as well as a  test mode flag and additional test arguments.

    Args:
        scenarioFilePath (str): The file path of the scenario file that contains the test cases.
        inIDSList (list): A list of input IDS names that should be read from the scenario file.
        outIDSList (list): A list of output IDS names  It is used to specify the list of output IDs that the function should read from the scenario file. If this parameter is not provided, the function will read all output IDs from the scenario file.
        testMode (bool): A boolean flag indicating whether the function is being called in test mode or not. If testMode is True, the function will execute in a way that is suitable for testing purposes. Defaults to False
    """
    testArgsList = list(testArgs.values())

    inIDSDict = {}
    outIDSDict = {}
    if inIDSList is None:
        inIDSList = []

    if outIDSList is None:
        outIDSList = []
    with open(scenarioFilePath, "r") as scenario_file:
        config = yaml.load(scenario_file, Loader=yaml.CLoader)

    # Read the equilibrium and core_profiles IDSs from the input datafile
    connectionIn = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["input_database"],
        config["shot"],
        config["run_in"],
        config["input_user_or_path"],
    )
    connectionIn.open()
    for idsName in inIDSList:
        if testMode:
            ids = connectionIn.get_slice(idsName, testArgsList)
        else:
            ids = connectionIn.get(idsName)
        inIDSDict[idsName] = ids

    connectionIn.close()

    # Read the out IDS from the output datafile
    connectionOut = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["output_database"],
        config["shot"],
        config["run_out"],
        os.getenv("USER")
        if config["output_user_or_path"] == "default"
        else config["output_user_or_path"],
    )
    print(config["output_database"])
    print(config["shot"])
    print(config["run_out"])
    print(config["output_user_or_path"])
    connectionOut.open()
    for idsName in outIDSList:
        if testMode:
            ids = connectionOut.get_slice(idsName, testArgsList)
        else:
            ids = connectionOut.get(idsName)
        outIDSDict[idsName] = ids
    connectionOut.close()

    return inIDSDict, outIDSDict


class Connection:
    def __init__(self, backend, database, shot, run, user, version):
        self.backend = backend
        self.database = database
        self.shot = shot
        self.run = run
        self.user = user
        self.version = version
