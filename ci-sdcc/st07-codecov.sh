#!/bin/bash
# Bamboo CI script to test IDS tools on different toolchains
# Execute script from root directory
source ./ci-sdcc/st00-header.sh $1 $2

# Note Disable set -e option when using on local as it will exit the shell on error
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    set -e -u -o pipefail
fi

ENVIRONEMNT_NAME=env"$TOOLCHAIN_VERSION"_"$ACCESS_LAYER_VERSION"
module unload IDStools

python -m venv "$ENVIRONEMNT_NAME"

. "$ENVIRONEMNT_NAME"/bin/activate
pip install coverage
# run tests
coverage run --source=idstools -m pytest tests

# report
coverage report -i
deactivate
rm -rf "$ENVIRONEMNT_NAME"
echo "Done"