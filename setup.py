#!/usr/bin/env python
import pathlib
import os
from setuptools import setup
from setuptools import find_packages

import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

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
    include_package_data=True,
    scripts=[
        "scripts/dbscraper",
        "scripts/dbselector",
        "scripts/dblist",
        "scripts/pulsecomposition",
        "scripts/plotequilibrium",
        "scripts/idscat",
        "scripts/idscp",
        "scripts/idsdiff",
        "scripts/idslist"
    ]
    # data_files=data_files,
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
