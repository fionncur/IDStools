# src/database/functions.py ok
import imas
import pandas as pd
import os, imas, yaml

progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print("Install tqdm to enable progress bar")
    progbar = False


class DatabaseTools:
    def __init__(self):
        pass

    @staticmethod
    def getIdsDataFrameFromPulseDatabase(
        dbuser: str,
        database: str,
        version: str,
        backend: int,
        idspath: str,
        pulses: tuple,
    ) -> pd.DataFrame:
        """
        This function retrieves pandas dataframe displaying all values of given IDSs extracted by the function.

        Args:
            dbuser (str): The username to access the Pulse database. A public user should just be left as public, whereas a local user should write their proper identifier
            database (str): The name of the database where the data is harbored
            version (str): String of number of data version
            backend (int): ID of backend of the database in which the data is harbored
            idspath (str): IDS path (starting with IDS name) to the desired data to be collected (e.g 'equilibrium/time')
            pulses (tuple): List of tuples containing (Pulse, Run)

        Returns:
            a pandas DataFrame containing information about the specified pulses and their associated values from a pulse database.
        """
        idsname = idspath.split("/")[0]
        valpath = idspath[1 + len(idsname) :]
        dbtools = DatabaseTools()
        pulses = pulses[:4]
        values = [
            dbtools.getIdsDataFromPulseDatabase(
                backend,
                database,
                entry[0],
                entry[1],
                dbuser,
                version,
                idsname,
                valpath,
            )
            for entry in (tqdm(pulses) if progbar else pulses)
        ]
        df = pd.DataFrame(pulses, columns=["PULSE", "RUN"])
        df["VALUE"] = values
        return df

    def getIdsDataFromPulseDatabase(
        self, backend, database, pulse, run, dbuser, version, idsname, valpath
    ):
        connection = imas.DBEntry(backend, database, pulse, run, dbuser, version)
        connection.open()
        try:
            value = connection.partial_get(idsname, valpath)
        except Exception:
            value = None
        connection.close()
        return value


def readScenario(
    scenarioFilePath: str,
    inIDSList: list = None,
    outIDSList: list = None,
    testMode: bool = False,
    **testArgs
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
