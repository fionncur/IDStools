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


# Not executing on bamboo as it creates data entry in the home directory
# "eqdsk2ids -p 134174 -r 117 -c 11 -g resources/geqdsk/example.gfile -u $USERNAME -d ITER --log INFO"
# "idscp -sp 131024 -sr 10 -dp 145000 -dr 32 -u public"
# "idsresample -sp 131024 -sr 10 -dp 145000 -dr 2 -u public"
# "idsrescale_equilibrium -sp 134174 -sr 117 -dp 122222 -dr 22 --rescale 2"
# "idsshift_equilibrium -sp 122525 -sr 1 -dp 123001 -dr 21 --shift -0.01"
SCRIPTS=(
    "idschk -p 134174 -r 117 -f resources/validation_schemas/ITER/core_profiles.yml"
    "idsdiff summary -pulses 122502/1/public/MDSPLUS/ITER/3 122502/2/public/MDSPLUS/ITER/3"
    "idsdiff summary -pulses 130011/6/public/MDSPLUS/ITER/3 130012/4/public/MDSPLUS/ITER/3"
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


