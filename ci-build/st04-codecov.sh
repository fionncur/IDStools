#!/bin/bash
# Bamboo script
# Stage 4 : Code coverage of unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

# Unzip artifact
tar -xvzf ${PREFIX_DIR}.tar.gz ./${PREFIX_DIR}

# run tests
export PYVERSION=$(python3 -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
echo "PYVERSION :" $PYVERSION
export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}")/lib/python${PYVERSION}/site-packages:${PYTHONPATH}
echo "PYTHONPATH :" $PYTHONPATH | grep -i idstools
export PATH=$(get_abs_filename "./${PREFIX_DIR}")/bin:${PATH}
echo "PATH :" $PATH | grep -i idstools

# run tests
coverage run --source=idstools -m pytest tests

# report
coverage report -i