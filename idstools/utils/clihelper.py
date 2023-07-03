import argparse
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
