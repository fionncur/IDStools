try:
    from ._version import (
        version as __version__,  # noqa: F401 # pylint: disable=import-error
    )
    from ._version import version_tuple  # noqa: F401 # pylint: disable=import-error
except ImportError:
    __version__ = "unknown"
    version_tuple = (0, 0, 0)
