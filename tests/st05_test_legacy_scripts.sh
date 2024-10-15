#!/bin/bash
# Bamboo test execution script for analysis scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -p expand_aliases

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

SCRIPTS=(
    "eqdsk2ids -c 11 --src \"imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3\" -g resources/geqdsk/example.gfile --dest \"imas:hdf5?user=$USERNAME;pulse=134174;run=117;database=ITER;version=3?path=$DATABASE_DIR\" --log INFO"
    "eqdsk2ids -c 11 --src \"imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3\" -g resources/geqdsk/example.gfile --dest \"imas:hdf5?user=$USERNAME;pulse=134174;run=117;database=ITER;version=3?path=$DATABASE_DIR\" --log INFO"
    "idschk --uri \"imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3\" -f resources/validation_schemas/generic/core_profiles.yml"
    "validate_db_entry -s 134174 -r 117 --path resources/validation_schemas")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        return "$STATUS"
    fi
fi
