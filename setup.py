#!/usr/bin/env python

from setuptools import setup
import os, glob
import pathlib
import subprocess
import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")


# Generate list of python scripts
script_files = glob.glob("bin/*")
script_files.append("database_tools/ids_shift_eq.py")
script_files.append("database_tools/ids_rescale_eq.py")
script_files.append("database_tools/rosettacode.py")
script_files.append("idstools/idsdef.py")


# # Get version by PKGVERSION, .version file, or git describe
# def get_version():
#     version = os.getenv("PKGVERSION")
#     if not version and os.path.isfile(".version"):
#         version = open(".version").read()
#     if not version and os.path.isdir(".git"):
#         version = subprocess.check_output(["git", "describe"]).strip().decode("ascii")
#         if "-" in version:
#             p = version.split("-")
#             version = p[0] + ".dev" + p[1] + "+" + "".join(p[2:])
#     return version


setup(
    name="IDStools",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="IMAS Python tools for IDSs",
    author="ITER Organization",
    author_email="imas-support@iter.org",
    url="https://imas.iter.org/",
    packages=["idstools", "database_tools"],
    py_modules=[],
    scripts=script_files,
    keywords="IMAS, IDS",
    data_files=[
        ("bin/mappings", ["database_tools/mappings/h-mode-db-mapping.csv"]),
        (
            "bin/validation_schemas",
            [
                "database_tools/validation_schemas/required_fields_core.yml",
                "database_tools/validation_schemas/required_fields_edge.yml",
            ],
        ),
    ],
)
