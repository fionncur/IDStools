#!/usr/bin/env python

from setuptools import find_packages, setup
import os, glob
import pathlib
import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")


# Generate list of python scripts
script_files = glob.glob("bin/*")
script_files.extend(
    (
        "database_tools/ids_shift_eq.py",
        "database_tools/ids_rescale_eq.py",
        "database_tools/rosettacode.py",
        "idstools/idsdef.py",
    )
)
files = [f for f in glob.glob("scripts/*") if os.path.isfile(f)]
script_files.extend(files)


setup(
    name="IDStools",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="IMAS Python tools for IDSs",
    author="ITER Organization",
    author_email="imas-support@iter.org",
    url="https://imas.iter.org/",
    classifiers=[
        "Development Status :: 2 - Beta",
        "Intended Audience :: Users/Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=find_packages(),
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


