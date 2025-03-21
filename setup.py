#!/usr/bin/env python3
###########################################################
# pip install .
#
# install docs requirements
# pip install .[docs]
# build docs
# pip install builddocs
###########################################################
import os
import pathlib
from glob import glob
from typing import Dict, List

from setuptools import Command, find_packages, setup
import versioneer

current_directory = pathlib.Path(__file__).parent.resolve()


class BuildDocs(Command):
    description = "Build Sphinx documentation"
    user_options = [
        ("format=", "f", "Provide format of the documentation (html or man)")
    ]

    def initialize_options(self):
        self.format = "html"

    def finalize_options(self):
        if self.format not in ["html", "man"]:
            raise ValueError("Please provide valid format ['html' or 'man']")

    def run(self):
        from sphinx.cmd.build import main as sphinx_main

        source_dir = os.path.join(current_directory, "docs", "source")
        build_dir = os.path.join(current_directory, "docs", "_build")
        sphinx_args = ["-b", self.format, source_dir, build_dir]
        sphinx_main(sphinx_args)


long_description = (current_directory / "README.md").read_text(encoding="utf-8")
requirements = f"{current_directory}/requirements.txt"
requirementsdocs = f"{current_directory}/docs/requirements.txt"


def getRequirements(filename):
    with open(filename, "r") as f:
        return f.read().splitlines()


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
    man_path = os.path.join(current_directory, "docs/_build/man/idstools.1")
    if os.path.exists(man_path):
        data_files.append(("share/man/man1/", [man_path]))

    scientific_mplstyle = os.path.join(
        current_directory, "idstools/view/styles/scientific.mplstyle"
    )
    if os.path.exists(scientific_mplstyle):
        data_files.append(("share/styles/", [scientific_mplstyle]))
    return data_files


def getCmdClass():
    cmdclass = versioneer.get_cmdclass()
    cmdclass["builddocs"] = BuildDocs
    return cmdclass


setup(
    name="IDStools",
    version=versioneer.get_version(),
    cmdclass=getCmdClass(),
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
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=find_packages(),
    keywords="IMAS, IDS",
    install_requires=getRequirements(requirements),
    scripts=[
        "scripts/dbconverter",
        "scripts/dblist",
        "scripts/dbperf",
        "scripts/dbscraper",
        "scripts/dbselector",
        "scripts/eqdsk2ids",
        "scripts/idscp",
        "scripts/idsdiff",
        "scripts/idslist",
        "scripts/idsperf",
        "scripts/idsprint",
        "scripts/idsresample",
        "scripts/idsrescale_equilibrium",
        "scripts/idsrosettacode",
        "scripts/idssize",
        "scripts/idsshift_equilibrium",
        "scripts/plotcoresources",
        "scripts/plotecstrayradiation",
        "scripts/plotedgeprofiles",
        "scripts/plotequilibrium",
        "scripts/plotequicomp",
        "scripts/printfluxes",
        "scripts/plothcddistributions",
        "scripts/plothcd",
        "scripts/plotkineticprofiles",
        "scripts/plothcdwaves",
        "scripts/plotmachinedescription",
        "scripts/plotneutron",
        "scripts/printplasmacompo",
        "scripts/plotpressure",
        "scripts/plotscenario",
        "scripts/plotrotation",
        "scripts/printcoresources",
        "scripts/plotecray",
        "scripts/ploteccomposition",
        "scripts/plotspectrometry",
        "scripts/plotcoretransport",
        "scripts/create_db_entry",  # scenario db scripts
        "scripts/create_db_entry_disruption",
        "scripts/disruption_summary",
        "scripts/md_status",
        "scripts/md_summary",
        "scripts/scenario_status",
        "scripts/scenario_summary",
        "scripts/show_db_entry",
        "scripts/watch_db_entry",
        "scripts/idstools",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    data_files=getDataFiles(),
    extras_require={
        "docs": getRequirements(requirementsdocs),
    },
)
