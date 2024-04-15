#!/bin/bash
# Bamboo CI script to test IDS tools on different toolchains
# Execute script from root directory
source ./ci-build/utils.sh

##########################################################################################
#                     Set environment based on toolchain                                 #
##########################################################################################
. /usr/share/Modules/init/sh
module use /work/imas/etc/modules/all

module purge

# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# Get toolchain version
if [ -z "$1" ]; then
    TOOLCHAIN_VERSION="intel-2020b"
else
    TOOLCHAIN_VERSION="$1"
fi

# Get AL version
if [ -z "$2" ]; then
    ACCESS_LAYER_VERSION="4"
else
    ACCESS_LAYER_VERSION="$2"
fi

echo "Testing for $TOOLCHAIN_VERSION and Access Layer $ACCESS_LAYER_VERSION"

ENVIRONEMNT_NAME=env"$TOOLCHAIN_VERSION"_"$ACCESS_LAYER_VERSION"
IMAS_MODULE_VERSION=$(getIMASModuleName "$TOOLCHAIN_VERSION" "$ACCESS_LAYER_VERSION")
# load IMAS module first
module load "$IMAS_MODULE_VERSION"
module unload -f IDStools

rm -rf "$ENVIRONEMNT_NAME"
python -m venv "$ENVIRONEMNT_NAME"

. "$ENVIRONEMNT_NAME"/bin/activate
python --version
pip install --upgrade pip
pip install .
export  PYTHONPATH
echo "Testing ids manipulation scripts"
source ./tests/st01_test_ids_scripts.sh 
echo ""
echo "Testing db scripts"
source ./tests/st02_test_db_scripts.sh 
echo ""
echo "Testing analysis scripts"
source ./tests/st03_test_analysis_scripts.sh 
echo ""
deactivate
rm -rf "$ENVIRONEMNT_NAME"

echo "done"