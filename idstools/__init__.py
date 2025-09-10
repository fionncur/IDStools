import os
import inspect
import subprocess
from typing import Optional

try:
    import imaspy as imas
except ImportError:
    import imas


try:
    from ._version import version as __version__  # noqa: F401
    from ._version import version_tuple  # noqa: F401
except ImportError:
    __version__ = "unknown"
    version_tuple = (0, 0, 0)


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


def get_version() -> str:
    """
    Return the version string of the 'idstools' module.
    If the module cannot be imported or has no '__version__', return ''.
    """
    try:
        import idstools

        version: Any = getattr(idstools, "__version__", "")
        return str(version) if version else ""
    except Exception:
        return ""


def get_git_hash() -> str:
    """
    Return the Git commit hash of the directory containing the running file.
    If the directory is not under Git control or any error occurs, return ''.
    """
    try:
        current_frame = inspect.currentframe()
        if current_frame is None:
            return ""
        caller_globals = current_frame.f_back.f_globals if current_frame.f_back else {}
        file_path: Optional[str] = caller_globals.get("__file__")
        if not file_path:
            return ""
        dir_path: str = os.path.dirname(os.path.abspath(file_path))
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["git", "-C", dir_path, "rev-parse", "HEAD"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=True,
            text=True,
        )
        return result.stdout.strip()
    except Exception:
        return ""
