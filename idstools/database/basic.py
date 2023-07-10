import os
from datetime import datetime
from glob import glob
from pathlib import Path
import fnmatch

import imas
import yaml


class DBMaster:
    ALL_BACKENDS = "mdsplus", "hdf5"

    @staticmethod
    def getUserDir(user: str = None):
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
        userDir = DBMaster.getUserDir(user)
        databases = [
            _database
            for _database in os.listdir(userDir)
            if os.path.isdir(os.path.join(userDir, _database))
        ]
        return sorted(databases)

    @staticmethod
    def getVersions(database:str, user: str = None) -> list:
        databaseDir = DBMaster.getDatabaseDir(database, user)
        versions = [
            _version
            for _version in os.listdir(databaseDir)
            if os.path.isdir(os.path.join(databaseDir, _version))
        ]
        return sorted(versions)

    @staticmethod
    def getDatabasesWithVersions(user: str = None) -> list:
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
            pulse = int(str(hdf5MasterFilePath).split("/")[-3])
            run = int(str(hdf5MasterFilePath).split("/")[-2])
            fileTime = datetime.fromtimestamp(os.path.getmtime(hdf5MasterFilePath)).replace(microsecond=0)

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
                        fileTime
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
        mdsplusDir = DBMaster.getVersionDir(version, database, user)
        pulses = {} if asDictionary else []

        for root, dirnames, filenames in os.walk(mdsplusDir):
            for datafile in fnmatch.filter(filenames, '*.datafile'):
                dataFilePath = f"{root}/{datafile}"
                if (status is None) or (
                    status
                    == DBMaster.getPulseStatus(Path(dataFilePath).with_suffix(".yaml"))
                ):
                    runList = (root[len(mdsplusDir)+1:]).split('/')
                    if len(runList)==1: #AL4 layout
                        numStartPos = datafile.find( '_' ) + 1
                        numEndPos = datafile.rfind( '.' )
                        num = int( datafile[numStartPos:numEndPos] )
                        pulse = num // 10000
                        run = int( runList[0] ) * 10000 + (num % 10000)
                    else: #AL5 layout
                        assert(datafile=="ids_001.datafile")
                        if os.path.islink(dataFilePath):
                            continue
                        run = root.split('/')[-1]
                        run = int(run)
                        pulse = root.split('/')[-2]
                        pulse = int(pulse)

                    fileTime = datetime.fromtimestamp(os.path.getmtime(dataFilePath)).replace(microsecond=0)
                    
                    if asDictionary:
                        if pulse not in pulses:
                            pulses[pulse] = []
                        isRunAvailable=False
                        for x in pulses[pulse]:
                            if x[1]==run:
                                isRunAvailable = True
                        if isRunAvailable is False:
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
                                fileTime
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
        result = []

        if not backends:
            backends = DBMaster.ALL_BACKENDS

        databases = [database] if database else DBMaster.getDatabases(user)
        for database in databases:
            databaseFiles = []
            versions = (
                [version] if version else DBMaster.getVersions(database, user)
            )
            for _version in versions:
                pulses = []
                for backend in backends:
                    if backend == "hdf5":
                        dbs = DBMaster.getHdf5Pulses(user, database, _version, asDictionary=True)
                    elif backend == "mdsplus":
                        dbs = DBMaster.getMdsPlusPulses(user, database, _version,  asDictionary=True)
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
        hdf5dir = os.path.join(DBMaster.getUserDir(user), database, version, "hdf5")
        return os.path.join(hdf5dir, f"ids_{str(pulse)}_{str(run)}.hd5")

    @staticmethod
    def getMDSPlusPhysicalFiles(user, database, version, pulse, run):
        """Return the MDS+ database filenames for a given IMAS database"""

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
        """Return files storing this database."""
        if backend == "mdsplus":
            return DBMaster.getMDSPlusPhysicalFiles(user, database, version, pulse, run)
        elif backend == "hdf5":
            return DBMaster.getHDF5PhysicalFile(user, database, version, pulse, run)
        else:
            raise NotImplementedError(f"Unsupported backend: {backend}")


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
    connectionOut.open()
    for idsName in outIDSList:
        if testMode:
            ids = connectionOut.get_slice(idsName, testArgsList)
        else:
            ids = connectionOut.get(idsName)
        outIDSDict[idsName] = ids
    connectionOut.close()

    return inIDSDict, outIDSDict
