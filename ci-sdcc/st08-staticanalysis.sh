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
# Install and run linters
pip install --upgrade 'black >=24,<25' flake8 pylint

echo "---------------------------------------------------------------------"
black --check imaspy > black.log
echo "---------------------------------------------------------------------"
flake8 imaspy > flake8.log
echo "---------------------------------------------------------------------"
pylint -E ./idstools > pylint.log
echo "---------------------------------------------------------------------"
deactivate
rm -rf "$ENVIRONEMNT_NAME"
echo "Done"



