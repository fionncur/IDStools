import os
import sys
import imas
from idstools.cli import get_backend_id


class DataProvider:
    """
    Short methods of calling IMAS functions and having responsibility of retreving data

    """

    def __init__(self, backend, database, shot, run, user):
        self.connection = self.connect(backend, database, shot, run, user)
        self.database_path = self.get_database_path(database, user)

    def connect(self, backend, database, shot, run, user):
        connection = imas.DBEntry(get_backend_id(backend), database, shot, run, user)
        err, n = connection.open()
        if err != 0:
            # TODO chek if you can raise exception or just print or may be use logger
            print(
                "Shot {0}, run {1} for user={2} and database={3} does not exists".format(
                    shot, run, user, database
                ),
                file=sys.stderr,
            )
            print("----> Aborted.", file=sys.stderr)
            exit()
        return connection

    def get_database_path(self, database, user):
        if user == "public":
            database_abs_path = (
                os.environ["IMAS_HOME"] + "/shared/imasdb/" + database + "/3"
            )
        else:
            database_abs_path = (
                os.path.expanduser("~{}".format(user))
                + "/public/imasdb/"
                + database
                + "/3"
            )
        return database_abs_path

    def get_ids(self, ids_name):
        try:
            ids_object = eval("imas." + ids_name + "()")

        except Exception as exc:
            print(
                "Can not retrieve the "
                + ids_name
                + " IDS from the input data-entry: {}".format(exc),
                file=sys.stderr,
            )
            print("----> Aborted.", file=sys.stderr)
            exit()
        return ids_object

    def get_time(self, ids_name, occurrence):
        return self.connection.partial_get(ids_name, "time", occurrence)

    def get_time_slice(self, ids_name, time_index, occurrence):
        return self.connection.partial_get(
            ids_name, "time_slice(" + str(time_index) + ")", occurrence
        )
