#!/usr/bin/env python


from setuptools import setup
import os, glob
import pathlib
import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()
long_description = (current_directory / "README.md").read_text(encoding="utf-8")

requirement_path = f"{current_directory}/requirements.txt"
install_requires = []
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()
        
# Generate list of python scripts
script_files = glob.glob("bin/*")
script_files.append("database_tools/ids_shift_eq.py")
script_files.append("database_tools/ids_rescale_eq.py")
script_files.append("database_tools/rosettacode.py")
script_files.append("database_tools/db_converter.py")
script_files.append("database_tools/db_extractor.py")
script_files.append("idstools/idsdef.py")

# Generate list of data files
source_folder = "database_tools"
target_folder = "bin"
types = ("*.yml", "*.csv")  # the tuple of file types

files_grabbed = []
for typename in types:
    files_grabbed.extend(glob.glob(source_folder + "/**/" + typename, recursive=True))

# create dictionary from glob files
files = {}
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

setup(
    name="iteridstools",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="IMAS IDS Python tools",
    author="ITER Organization",
    author_email="imas-support@iter.org",
    url="https://imas.iter.org/",
    packages=["idstools", "database_tools"],
    py_modules=[],
    scripts=script_files,
    keywords="IMAS, IDS",
    install_requires=install_requires,
    data_files=data_files,
)
