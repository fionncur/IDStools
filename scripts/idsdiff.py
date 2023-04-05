# #!/usr/bin/env python
import datetime
import logging
import imas
from idstools.cli import *

root_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(root_path)
from src.compute.common.functions import compare_ids


def setup_logger(name, verbose=False, log_dir="."):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARN)  # default
    if verbose:
        logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    # Create stream handler for logging to stdout (log all five levels)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stdout_handler)
    # enable_console_output()

    """Add a file handler for this logger with the specified `name` (and store the log file
    under `log_dir`)."""
    # Format for file log
    fmt = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(fmt)

    file_name = get_log_filename(name, log_dir)

    log_file = file_name + ".log"

    # Create file handler for logging to a file (log all five levels)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger, file_name


def get_log_filename(name, log_dir):
    # Determine log path and file name; create log path if it does not exist
    now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_name = f'{str(name).replace(" ", "_")}_{now}'
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except:
            print(
                f"Cannot create directory {log_dir}. ",
                end="",
                file=sys.stderr,
            )
            log_dir = "/tmp" if sys.platform.startswith("linux") else "."
            print(f"Defaulting to {log_dir}.", file=sys.stderr)
    return os.path.join(log_dir, log_name)


if __name__ == "__main__":
    logger, file_name = setup_logger("module", verbose=True, log_dir="logs")
    logger.info("logger is initiated")
    # Management of input arguments
    parser = argparse.ArgumentParser(
        description="Compare a IDS from 2 datasets", parents=[imas_parser]
    )
    parser.add_argument("shotA", type=int, help="shot number of first dataset")
    parser.add_argument("runA", type=int, help="run number of first dataset")
    parser.add_argument("shotB", type=int, help="shot number of second dataset")
    parser.add_argument("runB", type=int, help="run number of second dataset")
    parser.add_argument(
        "ids",
        nargs="*",
        type=str,
        help="Name (or space separated list of names) of IDS to compare (leave empty to compare all IDSs)",
    )
    parser.add_argument(
        "--backendB",
        type=str,
        default=None,
        help="Specifies the backend of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--databaseB",
        type=str,
        default=None,
        help="Specifies the database name of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--userB",
        type=str,
        default=None,
        help="Specifies the owner (username) of second dataset (default: same as first dataset)",
    )
    parser.add_argument(
        "--skip-provenance",
        action="store_true",
        help="Discards provenance data differences (optional)",
    )

    args = parser.parse_args()

    # set defaults for second dataset
    if args.databaseB is None:
        args.databaseB = args.database
    if args.backendB is None:
        args.backendB = args.backend
    if args.userB is None:
        args.userB = args.user

    inputA = imas.DBEntry(
        get_backend_id(args.backend),
        args.database,
        args.shotA,
        args.runA,
        user_name=args.user,
    )
    status, _ = inputA.open()
    if status != 0:
        logger.error(
            "Error opening first dataset! Please check existence.", file=sys.stderr
        )
        sys.exit(status)

    inputB = imas.DBEntry(
        get_backend_id(args.backendB),
        args.databaseB,
        args.shotB,
        args.runB,
        user_name=args.userB,
    )
    status, _ = inputB.open()
    if status != 0:
        logger.error(
            "Error opening second dataset! Please check existence.", file=sys.stderr
        )
        sys.exit(status)

    if args.ids == []:
        args.ids = [ids.value for ids in list(imas.IDSName)]
    file_object = open(file_name + ".csv", "w")
    import csv

    writer = csv.writer(file_object)
    writer.writerow(["Description", "Values"])
    for idsname in args.ids:
        idsA = inputA.get(idsname)
        idsB = inputB.get(idsname)

        compare_ids(
            idsA,
            idsB,
            field=idsname,
            ignore_version=args.skip_provenance,
            file_object=file_object,
        )
    file_object.close()
