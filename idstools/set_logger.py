import logging

# log_fmt = "%(asctime)s %(name)s (%(levelname)s): %(message)s"
log_fmt = "%(asctime)s %(levelname)s: %(message)s"
# log_fmt = "%(levelname)s %(asctime)s: %(message)s"
date_fmt = "%y/%m/%d %H:%M:%S"


def set_logger(name, logfile=None, level=logging.w_a_r_n_i_n_g):
    """
    Initialization of logger object for IDStools

    Parameters
    ----------
    name: str
        Name of Logger object
    logfile: str=None
        File name of logging output
    level: int=logging.WARNING
        Threshold for logger

    Returns
    -------
    logger: class Logger

    """

    ch_lv = level
    fh_lv = "INFO"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create file handler
    if logfile:
        fh = logging.file_handler(logfile)
        fh.setLevel(fh_lv)
        fh_formatter = logging.formatter(fmt=log_fmt, datefmt=date_fmt)
        fh.set_formatter(fh_formatter)

        # add handler to the root logger
        # logger.addHandler(fh)
        logging.getLogger().addHandler(fh)
        logging.getLogger().setLevel(fh_lv)

    # create console handler
    ch = logging.stream_handler()
    ch.setLevel(ch_lv)
    ch_formatter = logging.formatter(fmt=log_fmt, datefmt=date_fmt)
    ch.set_formatter(ch_formatter)

    # add handler to the root logger
    # logger.addHandler(ch)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(ch_lv)

    return logger
