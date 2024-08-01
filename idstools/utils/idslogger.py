import logging
import sys

try:
    from rich.console import Console
    from rich.logging import RichHandler

    rich_available = True
except ImportError:
    rich_available = False


def setup_logger(
    name,
    log_file=None,
    log_file_level=logging.DEBUG,
    stdout_level=logging.WARN,
    fmt=None,
):
    # Format for file log
    if fmt is None:
        fmt = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(fmt)

    logger = logging.getLogger(name)
    logger.setLevel(stdout_level)
    # Create stream handler for logging to stdout (log all five levels)
    if rich_available:
        console = Console()
        handler = RichHandler(console=console)
        handler.setLevel(stdout_level)
        logger.addHandler(handler)
    else:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(stdout_level)
        stdout_handler.setFormatter(logging.Formatter("%(message)s"))
        logger.addHandler(stdout_handler)

    # Create file handler for logging to a file (log all five levels)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger
