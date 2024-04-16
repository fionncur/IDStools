#!/bin/bash
# Bamboo test execution script for ids manipulation scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -p expand_aliases

#print hostname
hostname -f

#Get user name
USERNAME=$(whoami)

# create log directory
LOG_DIR=$PWD/"logs"
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"

SCRIPTS=(
    "eqdsk2ids -p 134174 -r 117 -g resources/geqdsk/example.gfile -u $USERNAME -d ITER --log INFO"
    "idschk -p 134174 -r 117 -f resources/validation_schemas/ITER/core_profiles.yml"
    "idscp -pi 131024 -ri 10 -po 145000 -ro 2 -u public" 
    "idsdiff --pulseA 122525 --runA  1 --pulseB 122525 --runB 2 summary"
    "idsdiff --pulseA 130011 --runA  6 --pulseB 130012 --runB 4 summary"
    "idsresample -pi 131024 -ri 10 -po 145000 -ro 2 -u public"
    "idsrescale_equilibrium -pi 122525 -ri 1 -po 122222 -ro 22 --rescale 2"
    "idsshift_equilibrium -pi 122525 -ri 1 -po 123001 -ro 1 --shift -0.01"
    "idslist -p 122525 -r 1"
    "idslist -p 122525 -r 1 yaml"
    "idslist -p 122525 -r 1 occ"
    "idsperf -p 122525 -r 1 equilibrium"
    "idsprint -p 122525 -r 1 equilibrium"
    "idssize -p 122525 -r 1 equilibrium"
    "idssize -p 131024 -r 10")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi


