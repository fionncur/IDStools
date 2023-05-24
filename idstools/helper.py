import os, fnmatch
import logging

""" Some helper methods."""


def is_sequence(arg):
    """Test whether an object behaves like a sequence.

    See http://stackoverflow.com/questions/1835018/python-check-if-an-object-is-a-list-or-tuple-but-not-string.
    """
    return (
        not hasattr(arg, "strip")
        and hasattr(arg, "__getitem__")
        or hasattr(arg, "__iter__")
    )


def make_sequence(arg):
    """Make sure an object is a sequence. If not, package it in a tuple."""
    if is_sequence(arg):
        return arg
    else:
        return (arg,)


def locate(pattern, root=os.curdir):
    """Locate all files matching supplied filename pattern in and below
    supplied root directory."""
    for path, dirs, files in os.walk(os.path.abspath(root)):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(path, filename)
            
            
def setup_logger(logger_name, level=logging.WARN):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
