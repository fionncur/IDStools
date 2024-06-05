#!/bin/bash
# Bamboo test execution script for ids manipulation scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

#Get user name
USERNAME=$(whoami)

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
    "eqdsk2ids -c 11 --src \"imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3\" -g resources/geqdsk/example.gfile --dest \"imas:mdsplus?user=$USERNAME;pulse=134174;run=117;database=ITER;version=3?path=$DATABASE_DIR\" --log INFO"
    "idschk --uri \"imas:mdsplus?user=public;pulse=134174;run=117;database=ITER;version=3\" -f resources/validation_schemas/generic/core_profiles.yml"
    "idscp --src \"imas:mdsplus?user=public;pulse=131024;run=10;database=ITER;version=3\" --dest \"imas:mdsplus?user=$USERNAME;pulse=145000;run=5;database=ITER;version=3?path=$DATABASE_DIR\""
    "idsdiff summary --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" \"imas:mdsplus?user=public;pulse=122525;run=2;database=ITER;version=3\""
    "idsdiff summary --uri \"imas:mdsplus?user=public;pulse=130011;run=6;database=ITER;version=3\" \"imas:mdsplus?user=public;pulse=130012;run=4;database=ITER;version=3\""
    "idsresample --src \"imas:mdsplus?user=public;pulse=131024;run=10;database=ITER;version=3\" --dest \"imas:mdsplus?user=$USERNAME;pulse=131024;run=5;database=ITER;version=3?path=$DATABASE_DIR\""
    "idsrescale_equilibrium --src \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" --dest \"imas:mdsplus?user=$USERNAME;pulse=122222;run=22;database=ITER;version=3?path=$DATABASE_DIR\"  --rescale 2"
    "idsshift_equilibrium --src \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" --dest \"imas:mdsplus?user=$USERNAME;pulse=123001;run=1;database=ITER;version=3?path=$DATABASE_DIR\"  --shift -0.01"
    "idslist --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\""
    "idslist --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" -y"
    "idslist --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" -o"
    "idsperf --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" summary"
    "idsperf --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" summary --verbose --outputRun 5 --showStats --repeat 2"
    "idsperf --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" summary --verbose --outputRun 5 --showStats --repeat 2 --uriOut \"imas:mdsplus?user=$USERNAME;pulse=131024;run=25;database=ITER;version=3?path=$DATABASE_DIR\" --memoryBackend"
    "idsprint --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3#equilibrium\""
    "idssize --uri \"imas:mdsplus?user=public;pulse=122525;run=1;database=ITER;version=3\" equilibrium"
    "idssize --uri \"imas:mdsplus?user=public;pulse=131024;run=10;database=ITER;version=3\"")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi
