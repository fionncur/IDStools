import os
from glob import glob
from typing import Dict, List

from setuptools import setup


# Generate list of data files
def getDataFiles():
    source_folder = "resources"
    target_folder = "bin"
    types = ("*.yml", "*.csv", "*.gfile", "*.txt", "*.yaml")  # the tuple of file types

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
    man_path = "docs/_build/man/idstools.1"
    if os.path.exists(man_path):
        data_files.append(("share/man/man1/", [man_path]))

    scientific_mplstyle = "idstools/view/styles/scientific.mplstyle"
    if os.path.exists(scientific_mplstyle):
        data_files.append(("share/styles/", [scientific_mplstyle]))
    return data_files


setup(
    data_files=getDataFiles(),
)
