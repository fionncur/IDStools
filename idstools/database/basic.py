import os
from glob import glob
from pathlib import Path

import imas
import yaml


class DBMaster:
    def __init__(self, user, database, version):
        """
        The function initializes an object with user, database, and version attributes, and sets the  locpath attribute based on the provided user, database, and version.

        Args:
            user: The "user" parameter represents the username of the user accessing the database. It can be either "public" or a specific username.
            database: The `database` parameter is a string that represents the name of the database. It is used to specify which database/tokamak to connect to or retrieve data from.
            version: The `version` parameter is used to specify the version of the database/tokamak that you want to access. It is a string that represents the version number or identifier of the database.
        """
        self.user = user
        self.database = database
        self.version = version
        self.locpath = None

        if user == "public":
            _locpath = (
                os.environ["IMAS_HOME"] + "/shared/imasdb/" + database + "/" + version
            )
        else:
            _locpath = (
                os.path.expanduser("~" + user)
                + "/public/imasdb/"
                + database
                + "/"
                + version
            )
        if os.path.exists(_locpath):
            self.locpath = _locpath
        else:
            raise FileNotFoundError(
                "The path provided does not exist or has no such database file or directory. Please check spelling."
            )

    def getHdf5Pulses(self):
        """
        The function `getHdf5Pulses` retrieves a list of pulses from HDF5 master files.

        Returns:
            a list of tuples. Each tuple contains the following elements, The tuple includes the pulse number, run number, HDF5_BACKEND backend, database, user, version, and data file path.
        """
        pulses = []
        hdf5MasterFilePaths = glob(f"{self.locpath}/**/*master.h5", recursive=True)
        for hdf5MasterFilePath in hdf5MasterFilePaths:
            pulse = int(str(hdf5MasterFilePath).split("/")[-3])
            run = int(str(hdf5MasterFilePath).split("/")[-2])
            pulses.append(
                (
                    pulse,
                    run,
                    imas.imasdef.HDF5_BACKEND,
                    self.database,
                    self.user,
                    self.version,
                    hdf5MasterFilePath,
                )
            )

        return pulses

    def getMdsPlusPulses(self, status=None):
        """
        The function `getMdsPlusPulses` retrieves a list of MDSPlus pulses based on the given status.

        Args:
            status: The `status` parameter is used to filter the pulses based on their status. If `status` is `None`, then all pulses are considered. Otherwise, only pulses with the specified status are included in the result.

        Returns:
            a list of tuples, where each tuple contains information about a pulse. The tuple includes the pulse number, run number, MDSPLUS backend, database, user, version, and data file path.
        """
        pulses = []
        datafilePaths = glob(f"{self.locpath}/**/*.datafile", recursive=True)
        for datafilePath in datafilePaths:
            if (status is None) or (
                status == self.getPulseStatus(Path(datafilePath).with_suffix(".yaml"))
            ):
                if os.path.islink(datafilePath):
                    continue
                pulseRunNumber = datafilePath.split("/")[-1].split("_")[1].split(".")[0]
                pulse = 0 if len(pulseRunNumber) <= 4 else int(pulseRunNumber[:-4])
                run = int(pulseRunNumber[-4:]) + 10000 * int(
                    datafilePath.split("/")[-2]
                )
                pulses.append(
                    (
                        pulse,
                        run,
                        imas.imasdef.MDSPLUS_BACKEND,
                        self.database,
                        self.user,
                        self.version,
                        datafilePath,
                    )
                )
        return pulses

    @staticmethod
    def getPulseStatus(path):
        """
        The function `getPulseStatus` reads a YAML file from a given path and returns the value of the
        "status" key in the file's metadata.

        Args:
            path: The `path` parameter is a string that represents the file path to a YAML file.

        Returns:
            the value of the "status" key from the metadata dictionary.
        """
        p = Path(path)
        try:
            with open(p, "r") as f:
                metadata = yaml.safe_load(f)
        except FileNotFoundError as exc:
            print(exc)
            return "unknown"
        return metadata["status"]


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
