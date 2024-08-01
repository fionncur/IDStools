import argparse
import os
import socket
import re
import imas
from imas import imasdef


def get_core_version():
    _lowlevel_version = ""
    if "_al_lowlevel" in imas.__dict__:
        _lowlevel_version = imas.get_al_version()
    if "_ual_lowlevel" in imas.__dict__:
        raw_core_version = imas._ual_lowlevel.__name__  # '__name__': 'imas_3_41_0_ual_4_11_10._ual_lowlevel
        raw_core_version, _ = raw_core_version.split(".")
        match = re.search(r"\d+_\d+_\d+$", raw_core_version)
        if match:
            _lowlevel_version = match.group()
            _lowlevel_version = _lowlevel_version.replace("_", ".")
    lowlevel_version = int(_lowlevel_version.split(".")[0])
    return lowlevel_version


# default parent parser for all idstools scripts
uri_parser = argparse.ArgumentParser(add_help=False)
uri_parser.add_argument(
    "-u",
    "--uri",
    type=str,
    required=True,
    help="uri",
)

imas_parser = argparse.ArgumentParser(add_help=False)
imas_parser.add_argument(
    "-u",
    "--user_or_path",
    dest="user",
    type=str,
    default="public",  # os.environ["USER"],
    help="user \t\t(default=%(default)s)",
)
db_group = imas_parser.add_mutually_exclusive_group()
db_group.add_argument(
    "-d",
    "--database",
    type=str,
    default="ITER",
    help="database name \t(default=%(default)s)",
)
imas_parser.add_argument(
    "-b",
    "--backend",
    type=str,
    default="MDSPLUS",
    help="backend format \t(default=%(default)s)",
)
imas_parser.add_argument(
    "-v",
    "--version",
    type=str,
    default="3",
    help="data version \t(default=%(default)s)",
)

dbentry_parser = argparse.ArgumentParser(add_help=False, parents=[uri_parser])


def get_backend_id(name):
    return getattr(imasdef, f"{name}_BACKEND")


def get_slice_mode(name):
    return getattr(imasdef, f"{name}_INTERP")


def get_details_from_uri(uri):
    import re

    param = {}
    user_pattern = r"user=([^;]+)"
    database_pattern = r"database=([^;]+)"
    version_pattern = r"version=(\d+)"
    backend_pattern = r"imas:(.*?)\?"
    shot_pattern = r"shot=(\d+)"
    pulse_pattern = r"pulse=(\d+)"
    run_pattern = r"run=(\d+)"
    path_pattern = r"path=([^?]+)"

    user_match = re.search(user_pattern, uri)
    database_match = re.search(database_pattern, uri)
    version_match = re.search(version_pattern, uri)
    backend_match = re.search(backend_pattern, uri)
    shot_match = re.search(shot_pattern, uri)
    pulse_match = re.search(pulse_pattern, uri)
    run_match = re.search(run_pattern, uri)
    path_match = re.search(path_pattern, uri)

    param["user"] = user_match.group(1) if user_match else None
    param["database"] = database_match.group(1) if database_match else None
    param["version"] = version_match.group(1) if version_match else None
    param["backend"] = backend_match.group(1) if backend_match else None
    shot = shot_match.group(1) if shot_match else None
    pulse = pulse_match.group(1) if pulse_match else None
    param["pulse"] = None
    if shot is not None:
        param["pulse"] = int(shot)
    elif pulse is not None:
        param["pulse"] = int(pulse)
    param["run"] = run_match.group(1) if run_match else None
    if param["backend"] is not None:
        param["backend"] = param["backend"].upper()
    if param["run"] is not None:
        param["run"] = int(param["run"])
    if path_match:
        param["path"] = path_match.group(1)
        param["pathPresent"] = True
    else:
        param["pathPresent"] = False
    param["legacyPresent"] = True
    if (
        param["run"] is None
        or param["pulse"] is None
        or param["database"] is None
        or param["backend"] is None
        or param["user"] is None
        or param["version"] is None
    ):
        param["legacyPresent"] = False

    return param


def get_title(imasargs, title="", time_value=None):
    _title = ""
    if title:
        _title += f"{title} "
    if "uri" in imasargs.__dict__ and imasargs.uri:
        param = get_details_from_uri(imasargs.uri)
        if param["pathPresent"]:
            _title += f"PATH={param['path']}"
        else:
            _title += f"(PULSE={param['pulse']},{param['run']})"
    else:
        _title += f"(PULSE={imasargs.pulse},{imasargs.run})"
    if time_value:
        _title += f" TIME:{time_value:.1f}"
    return _title


def get_file_name(imasargs, title="", time_value=None):
    _file_name = ""
    if title:
        _file_name += f"{title}_"
    if "uri" in imasargs.__dict__ and imasargs.uri:
        param = get_details_from_uri(imasargs.uri)
        if param["pathPresent"]:
            _file_name += f"PATH_{param['path'].replace('/', '_')}_"
        else:
            _file_name += f"PULSE_{param['pulse']}_RUN_{param['run']}_"
    else:
        _file_name += f"PULSE_{imasargs.pulse}_RUN_{imasargs.run}_"
    if time_value:
        _file_name += f"TIME_{time_value:.1f}"
    _file_name += ".png"
    return _file_name


def get_database_path(imasargs, time_value=None) -> str:
    """
    The function `get_database_path` returns the absolute path of a database based on the provided arguments.

    Args:
        imasargs: The `imasargs` parameter is an object or dictionary that contains the following attributes:

    Returns:
        the absolute path of the database.
    """
    pulse_info = ""
    database_absolute_path = ""
    if "uri" in imasargs.__dict__ and imasargs.uri:
        database_absolute_path = imasargs.uri

    else:
        if imasargs.user == "public":
            publichome = os.getenv("IMAS_HOME", default="")
            if publichome is None:
                return None
            database_absolute_path = (
                f"{publichome}/shared/imasdb/{imasargs.database}/{imasargs.version}/{imasargs.run//10000}"
            )
        else:
            database_absolute_path = (
                f'{os.path.expanduser(f"~{imasargs.user}")}/public/imasdb/'
                f"{str(imasargs.database)}/{imasargs.version}/{imasargs.run//10000}"
            )
        pulse_info = f"pulse {imasargs.pulse},{imasargs.run}"
        database_absolute_path = database_absolute_path[:-2]
    time_string = ""
    if time_value:
        time_string = f"time:{time_value:.2f})"
    hostdir = f"{socket.gethostname()}:{database_absolute_path} "
    if pulse_info:
        hostdir += f"({pulse_info})"
    if time_string:
        hostdir += f"#{time_string}"
    #
    return hostdir
