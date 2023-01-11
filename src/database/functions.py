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
