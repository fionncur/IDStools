#!/bin/bash
# Bamboo test execution script for analysis scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# create log directory
if [ -z "$1" ]; then
    LOG_DIR=$PWD/"logs"
    mkdir -p "$LOG_DIR"
else
    LOG_DIR="$1"
fi

if [ -z "$2" ]; then
    DATABASE_DIR=$PWD/"db"
    mkdir -p "$DATABASE_DIR"
else
    DATABASE_DIR="$2"
fi

# "viewall database --uri \"imas:mdsplus?user=schneim;pulse=92436;run=271;database=jet;version=3\""
SCRIPTS=(
    "plotkineticprofiles --uri \"imas:mdsplus?path=/work/imas/shared/imasdb/ITER/3/134174/117\" --save --directory $LOG_DIR"
    "plotpressure --uri \"imas:mdsplus?path=/work/imas/shared/imasdb/ITER/3/134174/117\" --save --directory $LOG_DIR"
    "plotspectrometry --uri \"imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/134000/37\" --save --directory $LOG_DIR")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi
