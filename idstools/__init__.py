import imas

from ._version import version as __version__  # noqa: F401
from ._version import version_tuple  # noqa: F401

if not hasattr(imas, "ids_defs"):
    print(
        """
[ERROR] Detected an outdated version of the 'imas' module.

The installed 'imas' package appears to be an incompatible legacy version of the high-level
Python interface of the IMAS Access Layer.

To resolve this, remove / unload this version and re-install using:

    pip install imas-python

or load the appropriate environment module on your system, e.g.

    module load IMAS-Python

More info: https://pypi.org/project/imas-python/
"""
    )
    exit(1)
