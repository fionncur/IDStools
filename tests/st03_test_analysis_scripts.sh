#!/bin/bash
# Bamboo test execution script for ids manipulation scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# create log directory
LOG_DIR=$PWD/"logs"
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"

SCRIPTS=(
    # "dbconverter --u public --database TEST -do MYDB -bo MDSPLUS --validate"
    "dblist -u public -d TEST list" 
    "dblist -u public -d TEST list -c" 
    "dblist -u public -d TEST list -M" 
    "dblist databases" 
    "dblist dataversions" 
    "dbperf -d TEST" 
    "dbscraper \"core_profiles/profiles_1d(0)/electrons/temperature\" --verbose --list-count 2"  
    "dbselector -d TEST core_profiles --list-count 2" 
    "dbselector -d TEST summary --list-count 2")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi

