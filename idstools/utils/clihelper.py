import argparse
import os
import socket
import re
import imas
from imas import imasdef

def getCoreVersion():
    _lowlevelVersion=""
    if "_al_lowlevel" in imas.__dict__:
        _lowlevelVersion=imas.get_al_version()
    if "_ual_lowlevel" in imas.__dict__:
        rawCoreVersion=imas._ual_lowlevel.__name__ # '__name__': 'imas_3_41_0_ual_4_11_10._ual_lowlevel
        rawCoreVersion, _ = rawCoreVersion.split(".")
        match = re.search(r'\d+_\d+_\d+$', rawCoreVersion)
        if match:
            _lowlevelVersion = match.group()
            _lowlevelVersion=_lowlevelVersion.replace("_", ".")
    lowlevelVersion = int(_lowlevelVersion.split(".")[0])
    return lowlevelVersion

# default parent parser for all idstools scripts
uriParser = argparse.ArgumentParser(add_help=False)
uriParser.add_argument(
    "-uri",
    "--uri",
    type=str,
    help="uri \t\t(default=%(default)s)",
)
imasParser = argparse.ArgumentParser(add_help=False)
imasParser.add_argument(
    "-u",
    "--user_or_path",
    dest="user",
    type=str,
    default="public",  # os.environ["USER"],
    help="user \t\t(default=%(default)s)",
)
db_group = imasParser.add_mutually_exclusive_group()
db_group.add_argument(
    "-d",
    "--database",
    type=str,
    default="ITER",
    help="database name \t(default=%(default)s)",
)
imasParser.add_argument(
    "-b",
    "--backend",
    type=str,
    default="MDSPLUS",
    help="backend format \t(default=%(default)s)",
)
imasParser.add_argument(
    "-v",
    "--version",
    type=str,
    default="3",
    help="data version \t(default=%(default)s)",
)
parents = [imasParser]

if getCoreVersion() > 4:
    parents.append(uriParser)
dbentryParser = argparse.ArgumentParser(add_help=False, parents=parents)
dbentryParser.add_argument(
    "-p", "--pulse", dest="pulse", help="Pulse number", type=int
)
dbentryParser.add_argument("-r", "--run", help="Run number", type=int)


def getBackendID(name):
    return getattr(imasdef, f"{name}_BACKEND")


def getSliceMode(name):
    return getattr(imasdef, f"{name}_INTERP")


def getDetailsfromURI(uri):
    import re

    param = {}
    user_pattern = r"user=([^;]+)"
    database_pattern = r"database=([^;]+)"
    version_pattern = r"version=([^;]+)"
    shot_pattern = r"shot=(\d+)"
    run_pattern = r"run=(\d+)"
    path_pattern = r'path=(.*)'

    user_match = re.search(user_pattern, uri)
    database_match = re.search(database_pattern, uri)
    version_match = re.search(version_pattern, uri)
    shot_match = re.search(shot_pattern, uri)
    run_match = re.search(run_pattern, uri)
    path_match = re.search(path_pattern, uri)

    param["user"] = user_match.group(1) if user_match else None
    param["database"] = database_match.group(1) if database_match else None
    param["version"] = version_match.group(1) if version_match else None
    param["pulse"] = shot_match.group(1) if shot_match else None
    param["run"] = run_match.group(1) if run_match else None
    if path_match:
        param["path"] = path_match.group(1)
        param["pathPresent"] = True
    else:
        param["pathPresent"] = False
    
    return param


def getTitle(args, title="", timeValue=None):
    _title = ""
    if title:
        _title += f"{title} "
    if "uri" in args.__dict__ and args.uri:
        param = getDetailsfromURI(args.uri)
        if param["pathPresent"]:
            _title += f"(path={param['path']})"
        else:
            _title += f"(pulse={param['pulse']},{param['run']})"
    else:
        _title += f"(pulse={args.pulse},{args.run})"
    if timeValue:
        _title += f" time:{timeValue:.1f}"
    return _title


def getFileName(args, title="", timeValue=None):
    _fileName = ""
    if title:
        _fileName += f"{title}_"
    if "uri" in args.__dict__ and args.uri:
        param = getDetailsfromURI(args.uri)
        if param["pathPresent"]:
            _fileName += f"(path={param['path']})"
        else:
            _fileName += f"pulse_{param['pulse']}_run_{param['run']}_"
    else:
        _fileName += f"pulse_{args.pulse}_run_{args.run}_"
    if timeValue:
        _fileName += f"time_{timeValue:.1f}"
    _fileName += ".png"
    return _fileName


def getDatabasePath(args, timeValue=None) -> str:
    """
    The function `getDatabasePath` returns the absolute path of a database based on the provided arguments.

    Args:
        args: The `args` parameter is an object or dictionary that contains the following attributes:

    Returns:
        the absolute path of the database.
    """
    pulseInfo=""
    databaseAbsolutePath=""
    if "uri" in args.__dict__ and args.uri:
        databaseAbsolutePath=args.uri
        
    else:
        if args.user == "public":
            publichome = os.getenv("IMAS_HOME", default="")
            if publichome is None:
                return None
            databaseAbsolutePath = (
                f"{publichome}/shared/imasdb/{args.database}/{args.version}/{args.run//10000}"
            )
        else:
            databaseAbsolutePath = f'{os.path.expanduser(f"~{args.user}")}/public/imasdb/{str(args.database)}/{args.version}/{args.run//10000}'
        pulseInfo=f"pulse {args.pulse},{args.run}"
        databaseAbsolutePath = databaseAbsolutePath[:-2]
    timeString = ""
    if timeValue:
        timeString = f"time:{timeValue:.2f})"
    hostdir = f"{socket.gethostname()}:{databaseAbsolutePath} ({pulseInfo} {timeString})"
    #
    return hostdir
