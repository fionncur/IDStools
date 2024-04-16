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
# load IMAS module
module load "$IMAS_MODULE_VERSION"
module unload -f IDStools

python -m venv "$ENVIRONEMNT_NAME"

. "$ENVIRONEMNT_NAME"/bin/activate
PYTHON_VERSION=$(python --version)
version_script=$(cat <<END
import numpy as np
import scipy
import matplotlib

print("NumPy version:", np.__version__)
print("SciPy version:", scipy.__version__)
print("Matplotlib version:", matplotlib.__version__)
END
)
python3 -c "$version_script"

pip install --upgrade pip
pip install .

echo "Testing ids manipulation scripts with $IMAS_MODULE_VERSION and Python $PYTHON_VERSION"
source ./tests/st01_test_ids_scripts.sh 
echo "---------------------------------------------------------------------"
echo "Testing db scripts with $IMAS_MODULE_VERSION and Python $PYTHON_VERSION"
source ./tests/st02_test_db_scripts.sh 
echo "---------------------------------------------------------------------"
echo "Testing analysis scripts  with $IMAS_MODULE_VERSION and Python $PYTHON_VERSION"
source ./tests/st03_test_analysis_scripts.sh 
echo "---------------------------------------------------------------------"
echo "Run pytest for functions testing with $IMAS_MODULE_VERSION and Python $PYTHON_VERSION"
python3 -m pytest --junit-xml=logs/test_report.xml tests 
deactivate
rm -rf "$ENVIRONEMNT_NAME"

ARTIFACT="./testlog.tar.gz"
# Check if the *.tar.gz exists before attempting to remove it
if [ -f "$ARTIFACT" ]; then
    rm "$ARTIFACT"
    echo "$ARTIFACT removed successfully."
fi

# Create acrtifact
tar -cvzf testlog.tar.gz logs >/dev/null 2>&1
if [ -f "$ARTIFACT" ]; then
    echo "Artifact $ARTIFACT created successfully."
fi

# show contents of artifact
tar -tzvf testlog.tar.gz

# Cleanup

echo "Done"

