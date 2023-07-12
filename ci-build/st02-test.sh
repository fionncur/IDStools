#!/bin/bash
# Bamboo script
# Stage 2 : Unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

# run tests
cd tests
chmod +x testscripts.sh
try bash testscripts.sh
