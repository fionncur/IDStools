#!/bin/bash
# Bamboo script
# Stage 1 : Pip install

# Set up environment
source ci-build/st00-header.sh $* || exit 1

# Create a virtualized environment for installing idstools
if [ -d "${PREFIX_DIR}" ];
then
    try rm -r ${PREFIX_DIR}
fi

try mkdir ${PREFIX_DIR}

try rm -r build_venv

# Test install command
try python3 -m pip install . --target=${PREFIX_DIR} --upgrade

export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}"):${PYTHONPATH}
echo $PYTHONPATH

try python3 -c 'import sys; print("Python version in virtual env : %d.%d"% sys.version_info[0:2])'

try python3 -c "from idstools.idsdef import IDSDef; dd=IDSDef(); f = dd.query(\"amns_data\", None) "

try python3 setup.py bdist_wheel || echo "Command bdist_wheel may not be found, it is harmless." 
try python3 setup.py sdist


# Stash
tar -cvzf ${PREFIX_DIR}.tar.gz ./${PREFIX_DIR} ./dist

# Clean up
try rm -r ${PREFIX_DIR}
try rm -r dist