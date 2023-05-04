import logging
import argparse
from imas import imasdef


def setup_logger(logger_name, level=logging.WARN):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


# default parent parser for all idstools scripts
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
    "--database",
    "-d",
    type=str,
    default="ITER",
    help="database name \t(default=%(default)s)",
)
imas_parser.add_argument(
    "--backend",
    "-b",
    type=str,
    default="MDSPLUS",
    help="backend format \t(default=%(default)s)",
)
imas_parser.add_argument(
    "--version",
    "-v",
    type=str,
    default="3",
    help="data version \t(default=%(default)s)",
)


def get_backend_id(name):
    return getattr(imasdef, f"{name}_BACKEND")


def get_slice_mode(name):
    return getattr(imasdef, f"{name}_INTERP")
