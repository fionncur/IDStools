# src/database/functions.py ok
import imas
import pandas as pd

progbar = True
try:
    from tqdm import tqdm
except ModuleNotFoundError:
    print(f"Install tqdm to enable progress bar")
    progbar = False


class DatabaseTools:
    def __init__(self):
        pass

    @staticmethod
    def get_idsdata_in_dataframes_from_pulses(
        dbuser, database, version, backend, idspath, pulses
    ):
        """Function that returns a pandas dataframe displaying all values of given IDSs extracted by the function.

        Parameters
        ---------
        user: str
        Status of user: either public or local. A public user should just be left as public, whereas a local user should write their proper identifier

        database: str
            Name of database where the data is harbored

        version: str
            String of number of data version

        backend: int
            ID of backend of the database in which the data is harbored

        idspath: str
            IDS path (starting with IDS name) to the desired data to be collected (e.g 'equilibrium/time')

        pulses: list of tuples
            List of tuples containing (Pulse, Run)

        Returns
        -------
        pandas DataFrame
        """

        values = []
        idsname = idspath.split("/")[0]
        valpath = idspath[1 + len(idsname) :]
        dbtools = DatabaseTools()
        pulses = pulses[:4]
        for entry in tqdm(pulses) if progbar else pulses:
            values.append(
                dbtools.get_data_from_ids(
                    backend,
                    database,
                    entry[0],
                    entry[1],
                    dbuser,
                    version,
                    idsname,
                    valpath,
                )
            )

        df = pd.DataFrame(pulses, columns=["PULSE", "RUN"])
        df["VALUE"] = values
        return df

    def get_data_from_ids(
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



def read_ids(scenario_file_path):

    import os, imas, yaml

    testmode = 0
    # Initial values of time slice and beam index
    time_slice = 35.0
    beam_index = 6
    # Read scenario.yaml used for the simulation to know where to find
    # the IMAS output datafile
    scenario_file = open(scenario_file_path, "r")
    config = yaml.load(scenario_file, Loader=yaml.CLoader)
    scenario_file.close()

    # Find output datafile from the configuration parameters
    output_user_or_path = ""
    if config["output_user_or_path"] == "default":
        output_user_or_path = os.getenv("USER")
        config["output_user_or_path"] = os.getenv("USER")
    else:
        output_user_or_path = config["output_user_or_path"]

    # Read the equilibrium and core_profiles IDSs from the input datafile
    input = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["input_database"],
        config["shot"],
        config["run_in"],
        config["input_user_or_path"],
    )
    input.open()
    if testmode == 1:
        time_slice = 100.0
        equilibrium = input.get_slice("equilibrium", time_slice, 2)
        core_profiles = input.get_slice("core_profiles", 100.0, 2)
    else:
        equilibrium = input.get("equilibrium")
        core_profiles = input.get("core_profiles")

    input.close()

    # Read the waves IDS from the output datafile
    output = imas.DBEntry(
        imas.imasdef.MDSPLUS_BACKEND,
        config["output_database"],
        config["shot"],
        config["run_out"],
        config["output_user_or_path"],
    )
    output.open()
    if testmode == 1:
        waves = output.get_slice("waves", time_slice, 2)
    else:
        waves = output.get("waves")
    output.close()

    return equilibrium, core_profiles, waves
