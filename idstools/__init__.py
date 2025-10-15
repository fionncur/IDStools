try:
    import imaspy as imas
except ImportError:
    import imas


try:
    from ._version import (  # noqa: F401
        GIT_DATE,
        GIT_DESCRIBE,
        GIT_REV,
        __version__,
        version_tuple,  # noqa: F401
    )
except ImportError:
    __version__ = "unknown"
    version_tuple = (0, 0, 0)
    GIT_REV = GIT_DESCRIBE = GIT_DATE = "unknown"


if not hasattr(imas, "ids_defs"):
    print(
        """
[ERROR] Detected an outdated version of the 'imas' module.

The installed 'imas' package appears to be an incompatible legacy version of \
the high-level Python interface of the IMAS Access Layer.

To resolve this, remove / unload this version and re-install using:

    pip install imas-python

or load the appropriate environment module on your system, e.g.

    module load IMAS-Python

More info: https://pypi.org/project/imas-python/
"""
    )
    exit(1)
