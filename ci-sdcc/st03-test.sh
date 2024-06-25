#!/bin/bash
# Bamboo CI script to test IDS tools on different toolchains
# Execute script from root directory
source ./ci-sdcc/st00-header.sh $1 $2

# Note Disable set -e option when using on local as it will exit the shell on error
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    set -e -u -o pipefail
fi

ENVIRONEMNT_NAME=env"$TOOLCHAIN_VERSION"_"$ACCESS_LAYER_VERSION"
module unload -f IDStools

python -m venv "$ENVIRONEMNT_NAME"

. "$ENVIRONEMNT_NAME"/bin/activate

LOG_DIR="$PWD"/"$ENVIRONEMNT_NAME"/logs
mkdir -p "$LOG_DIR"

DB_DIR="$PWD"/"$ENVIRONEMNT_NAME"/db
mkdir -p "$DB_DIR"

#install packages
pip install --upgrade pip
pip install .
pip install packaging

PYTHON_VERSION=$(python --version)

# display versions
version_script=$(
    cat <<END
import numpy as np
import scipy
import matplotlib

print("NumPy version:", np.__version__)
print("SciPy version:", scipy.__version__)
print("Matplotlib version:", matplotlib.__version__)
END
)
echo "====================================================================="
python3 -c "$version_script"
echo "====================================================================="
#---------------------------------------------------------------------------
echo ""
echo ""

echo "====================================================================="
echo "Testing analysis scripts  with URI $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
source ./tests/st03_test_analysis_scripts_with_uri.sh "$LOG_DIR" "$DB_DIR"

echo "====================================================================="
echo "Testing analysis scripts  with URI PATH $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
source ./tests/st03_test_analysis_scripts_with_uripath.sh "$LOG_DIR" "$DB_DIR"
#---------------------------------------------------------------------------
echo ""
echo ""
echo "====================================================================="
echo "Testing ids manipulation scripts with $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
source ./tests/st01_test_ids_scripts_with_uri.sh "$LOG_DIR" "$DB_DIR"

# ---------------------------------------------------------------------------
echo ""
echo ""
echo "====================================================================="
echo "Testing db scripts with $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
source ./tests/st02_test_db_scripts.sh "$LOG_DIR" "$DB_DIR"

# ---------------------------------------------------------------------------
echo ""
echo ""
echo "====================================================================="
echo "Testing scenario scripts with $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
source ./tests/st04_test_scenario_scripts.sh "$LOG_DIR" "$DB_DIR"

echo ""
echo ""
echo "====================================================================="
echo "Run pytest for functions testing with $IMAS_MODULE_VERSION and $PYTHON_VERSION"
echo "====================================================================="
pip install pytest
python -m pytest --junit-xml="$LOG_DIR"/test_report.xml tests
echo "---------------------------------------------------------------------"
deactivate
rm -rf "$ENVIRONEMNT_NAME"

ARTIFACT=./$ENVIRONEMNT_NAME"_testlogs.tar.gz"
# Check if the *.tar.gz exists before attempting to remove it
if [ -f "$ARTIFACT" ]; then
    rm "$ARTIFACT"
    echo "$ARTIFACT removed successfully."
fi

# Create acrtifact
tar -cvzf "$ENVIRONEMNT_NAME"_testlogs.tar.gz "$LOG_DIR" >/dev/null 2>&1
if [ -f "$ARTIFACT" ]; then
    echo "Artifact $ARTIFACT created successfully."
fi

# show contents of artifact
tar -tzvf "$ENVIRONEMNT_NAME"_testlogs.tar.gz

# Cleanup

echo "Done"
