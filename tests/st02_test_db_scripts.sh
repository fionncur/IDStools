#!/bin/bash
# Bamboo test execution script for ids manipulation scripts
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

# Not executing on bamboo as it creates data entry in the home directory
# "dbconverter --u public --database TEST -do MYDB -bo MDSPLUS --validate"

SCRIPTS=(
    "dblist -u public -d TEST list" 
    "dblist -u public -d TEST list -c" 
    "dblist -u public -d TEST list -M" 
    "dblist -f /work/imas/shared/imasdb/TEST/3/ slices"
    "dblist -f /work/imas/shared/imasdb/TEST/3/ list"
    "dblist -f /work/imas/shared/imasdb/TEST/3/ --showuri list"
    "dblist databases" 
    "dblist dataversions" 
    "dbperf -d ITER --version 3 --pulse 134174 --run 117 --verb -exci core_sources equilibrium edge_profiles edge_sources core_transport core_profiles edge_transport"
    "dbscraper \"core_profiles/profiles_1d(0)/electrons/temperature\" --verbose --list-count 2"  
    "dbselector -d TEST core_profiles --list-count 2" 
    "dbselector -d TEST summary --list-count 2")

execute_scripts "${SCRIPTS[@]}"
return $?
