#!/bin/bash
# Bamboo script
# Stage 2 : Unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

tar xvf ${PREFIX_DIR}.tar.gz 
export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}"):${PYTHONPATH}
# run tests
pip install --prefix=${PREFIX_DIR} dist/*.whl --no-deps  --ignore-installed --no-index --upgrade
pytest  tests