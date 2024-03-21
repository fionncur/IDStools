import argparse
import os
import socket
import sys

from imas import imasdef

# default parent parser for all idstools scripts
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
    "--database",
    "-d",
    type=str,
    default="ITER",
    help="database name \t(default=%(default)s)",
)
imasParser.add_argument(
    "--backend",
    "-b",
    type=str,
    default="MDSPLUS",
    help="backend format \t(default=%(default)s)",
)
imasParser.add_argument(
    "--version",
    "-v",
    type=str,
    default="3",
    help="data version \t(default=%(default)s)",
)


def getBackendID(name):
    return getattr(imasdef, f"{name}_BACKEND")


def getSliceMode(name):
    return getattr(imasdef, f"{name}_INTERP")


def getDatabasePath(args) -> str:
    """
    The function `getDatabasePath` returns the absolute path of a database based on the provided arguments.

    Args:
        args: The `args` parameter is an object or dictionary that contains the following attributes:

    Returns:
        the absolute path of the database.
    """
    if args.user == "public":
        publichome = os.getenv("IMAS_HOME", default="")
        if publichome is None:
            return None
        databaseAbsolutePath = (
            f"{publichome}/shared/imasdb/{args.database}/{args.version}/{args.run//10000}"
        )
    else:
        databaseAbsolutePath = f'{os.path.expanduser(f"~{args.user}")}/public/imasdb/{str(args.database)}/{args.version}/{args.run//10000}'
    hostdir = f"{socket.gethostname()}:{databaseAbsolutePath}"
    hostdir = hostdir[:-2]
    return hostdir
