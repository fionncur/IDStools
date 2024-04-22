#!/bin/bash
# Bamboo script
# Set up environment such that module files can be loaded

. /usr/share/Modules/init/sh
# Purge modules and load IMAS module
module purge
module load IMAS
module unload -f IDStools

ENVIRONEMNT_NAME=envDocGen

# Create python virtual environment and install dependencies
rm -rf "$ENVIRONEMNT_NAME"
python -m venv "$ENVIRONEMNT_NAME"

. $ENVIRONEMNT_NAME/bin/activate
python --version
pip install --upgrade pip
pip install .
pip install -r docs/requirements.txt
pip list

# Build documentation
make -C docs realclean
make -C docs autogen
make -C docs html 
make -C docs man

deactivate
rm -rf "$ENVIRONEMNT_NAME"
