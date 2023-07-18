#!/bin/bash
# Bamboo script
# Stage 2 : Unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

tar xvf ${PREFIX_DIR}.tar.gz 

# run tests
chmod +x ${PREFIX_DIR}/tests/testscripts.sh
try bash ${PREFIX_DIR}/tests/testscripts.sh
