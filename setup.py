#!/usr/bin/env python3
import os
import pathlib
import subprocess

from setuptools import find_packages, setup

import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

requirement_path = f"{current_directory}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

data_files = []

# Create man page and append in data_files
subprocess.run([os.path.join(current_directory, "manpages.sh"), ""], shell=True)
man_path = os.path.join(current_directory, "docs/_build/man/idstools.1")
if os.path.exists(man_path):
    data_files.append(("share/man/man1/", [man_path]))


scientific_mplstyle = os.path.join(
    current_directory, "idstools/view/styles/scientific.mplstyle"
)
if os.path.exists(scientific_mplstyle):
    data_files.append(("share/styles/", [scientific_mplstyle]))

setup(
    name="IDSTools",
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
        "scripts/dblist",
        "scripts/dbscraper",
        "scripts/dbselector",
        "scripts/scenario_status",
        "scripts/scenario_summary",
        "scripts/md_status",
        "scripts/md_summary",
        "scripts/idscp",
        "scripts/idsdiff",
        "scripts/idslist",
        "scripts/idsperf",
        "scripts/idsprint",
        "scripts/idsresample",
        "scripts/idssize",
        "scripts/viewcoresources",
        "scripts/viewedgeprofiles",
        "scripts/viewequilibrium",
        "scripts/viewfluxes",
        "scripts/viewmachinedescription",
        "scripts/viewneutron",
        "scripts/viewplasmacompo",
        "scripts/viewpressure",
        "scripts/viewscenario",
        "scripts/viewrotation",
        "scripts/viewsources",
        "scripts/viewecray",
        "scripts/vieweccomposition",
        "scripts/viewwall",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    data_files=data_files,
)


# Generate list of python scripts
# script_files = glob.glob("bin/*")
# script_files.append("database_tools/ids_shift_eq.py")
# script_files.append("database_tools/ids_rescale_eq.py")
# script_files.append("database_tools/rosettacode.py")
# script_files.append("database_tools/db_converter.py")
# script_files.append("database_tools/db_extractor.py")
# script_files.append("idstools/idsdef.py")

# Generate list of data files
# source_folder = "database_tools"
# target_folder = "bin"
# types = ("*.yml", "*.csv")  # the tuple of file types

# files_grabbed = []
# for typename in types:
#     files_grabbed.extend(glob.glob(source_folder + "/**/" + typename, recursive=True))

# # create dictionary from glob files
# files = {}
# for file_path in files_grabbed:
#     folder_name = os.path.dirname(file_path)
#     folder_name = folder_name.replace(source_folder, target_folder)
#     if folder_name not in files.keys():
#         files[folder_name] = []
#     files[folder_name].append(file_path)

# # Create data structure which setup file is needed
# data_files = []
# for file_path, list_of_files in files.items():
#     data_files.append((file_path, list_of_files))
