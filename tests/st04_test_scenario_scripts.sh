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
    "md_status -s 116000 -r 3"
    "md_summary  -s 150502/102"
    "md_summary  -s nbi on-on"
    "scenario_status -s 134174 -r 117"
    "scenario_summary -s He4,2.65"
    "show_db_entry -s 134174 -r 117")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        return "$STATUS"
    fi
fi
