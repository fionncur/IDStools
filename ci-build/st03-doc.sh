#!/bin/bash
# Bamboo script
# Set up environment such that module files can be loaded
. /usr/share/Modules/init/sh
# Purge modules and load IMAS module
module purge
module load IMAS
# Create python virtual environment and install dependencies
rm -rf build_venv
python -m venv build_venv

. build_venv/bin/activate
python --version
pip install --upgrade pip
pip install -r docs/requirements.txt
pip list

# Build documentation
cd docs
make realclean
make autogen
make apidocs html 
cd ..
deactivate
rm -rf build_venv