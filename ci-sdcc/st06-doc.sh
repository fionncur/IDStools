#!/bin/bash
# Bamboo CI script to build actor and run standalone program
# Execute script from root directory
source /etc/profile.d/modules.sh
module use /work/imas/etc/modules/all
source ./ci-sdcc/st00-header.sh $1 $2 $3

# Note Disable set -e option when using on local as it will exit the shell on error
# if [[ "$(uname -n)" == *"bamboo"* ]]; then
#     set -e -u -o pipefail
# fi
IMAS_MODULE_VERSION=$(getIMASPythonModuleName "$TOOLCHAIN_VERSION" "$ACCESS_LAYER_VERSION" "$DD_VERSION")
module load $IMAS_MODULE_VERSION

ENVIRONEMNT_NAME=env"$TOOLCHAIN_VERSION"_"$ACCESS_LAYER_VERSION"

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
echo "Done"
