import logging
import sys

def setupLogger(
    name,
    log_file=None,
    log_file_level=logging.DEBUG,
    stdout_level=logging.WARN,
    fmt=None,
):
    logger = logging.getLogger(name)
    logger.setLevel(stdout_level)
    # Create stream handler for logging to stdout (log all five levels)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(stdout_level)
    stdout_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(stdout_handler)

    # Format for file log
    if fmt is None:
        fmt = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(fmt)

    # Create file handler for logging to a file (log all five levels)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
