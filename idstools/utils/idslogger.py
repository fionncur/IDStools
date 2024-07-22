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
    log_file_level=logging.d_e_b_u_g,
    stdout_level=logging.w_a_r_n,
    fmt=None,
):
    # Format for file log
    if fmt is None:
        fmt = "%(asctime)s | %(levelname)9s | %(filename)s:%(lineno)d | %(message)s"
    formatter = logging.formatter(fmt)

    logger = logging.getLogger(name)
    logger.setLevel(stdout_level)
    # Create stream handler for logging to stdout (log all five levels)
    if rich_available:
        console = console()
        handler = rich_handler(console=console)
        handler.setLevel(stdout_level)
        logger.addHandler(handler)
    else:
        stdout_handler = logging.stream_handler(sys.stdout)
        stdout_handler.setLevel(stdout_level)
        stdout_handler.set_formatter(logging.formatter("%(message)s"))
        logger.addHandler(stdout_handler)

    # Create file handler for logging to a file (log all five levels)
    if log_file:
        file_handler = logging.file_handler(log_file)
        file_handler.setLevel(log_file_level)
        file_handler.set_formatter(formatter)
        logger.addHandler(file_handler)
    return logger
