#!/usr/bin/env python3
from glob import glob
import os
import pathlib
import subprocess
from typing import Dict, List

from setuptools import find_packages, setup

import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

requirement_path = f"{current_directory}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()


# Generate list of data files
source_folder = "resources"
target_folder = "bin"
types = ("*.yml", "*.csv", "*.gfile")  # the tuple of file types

files_grabbed = []
for typename in types:
    files_grabbed.extend(glob(source_folder + "/**/" + typename, recursive=True))

# create dictionary from glob files
files: Dict[str, List] = {}
for file_path in files_grabbed:
    folder_name = os.path.dirname(file_path)
    folder_name = folder_name.replace(source_folder, target_folder)
    if folder_name not in files.keys():
        files[folder_name] = []
    files[folder_name].append(file_path)

# Create data structure which setup file is needed
data_files = []
for file_path, list_of_files in files.items():
    data_files.append((file_path, list_of_files))

# add man page if already created by script "manpages.sh"
man_path = os.path.join(current_directory, "docs/_build/man/idstools.1")
if os.path.exists(man_path):
    data_files.append(("share/man/man1/", [man_path]))


scientific_mplstyle = os.path.join(
    current_directory, "idstools/view/styles/scientific.mplstyle"
)
if os.path.exists(scientific_mplstyle):
    data_files.append(("share/styles/", [scientific_mplstyle]))

setup(
    name="IDStools",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Python based collection of data analysis and visualization tools written IMAS framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    keywords="IMAS, IDS",
    install_requires=install_requires,
    scripts=[
        "scripts/dbconverter",
        "scripts/dblist",
        "scripts/dbperf",
        "scripts/dbscraper",
        "scripts/dbselector",
        "scripts/eqdsk2ids",
        "scripts/idscp",
        "scripts/idschk",
        "scripts/idsdiff",
        "scripts/idslist",
        "scripts/idsperf",
        "scripts/idsprint",
        "scripts/idsresample",
        "scripts/idsrescale_equilibrium",
        "scripts/idsrosettacode",
        "scripts/idssize",
        "scripts/idsshift_equilibrium",
        "scripts/viewcoresourcesplot",
        "scripts/viewecstrayradiation",
        "scripts/viewedgeprofiles",
        "scripts/viewequilibrium",
        "scripts/viewfluxes",
        "scripts/viewhcddistributions",
        "scripts/viewhcdplots",
        "scripts/viewkineticprofiles",
        "scripts/viewhcdwaves",
        "scripts/viewmachinedescription",
        "scripts/viewneutron",
        "scripts/viewplasmacompo",
        "scripts/viewpressure",
        "scripts/viewscenario",
        "scripts/viewrotation",
        "scripts/viewcoresources",
        "scripts/viewecray",
        "scripts/vieweccomposition",
        "scripts/viewspectrometry",
        "scripts/viewcoretransport",
        "scripts/create_db_entry",  # scenario db scripts
        "scripts/create_db_entry_disruption",
        "scripts/create_validation_schema",
        "scripts/disruption_summary",
        "scripts/md_status",
        "scripts/md_summary",
        "scripts/scenario_status",
        "scripts/scenario_summary",
        "scripts/show_db_entry",
        "scripts/validate_db_entry",
        "scripts/watch_db_entry",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    data_files=data_files,
)
