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
    "viewcoresources -p 130012 -r 105 -d TEST  --save --directory $LOG_DIR"
    "viewcoretransport -p 92436 -r 850  -d TEST --save --directory $LOG_DIR"
    "vieweccomposition -p 134173 -r 2326 -d TEST --save --directory $LOG_DIR"
    "viewecray -p 134173 -r 2326 -d TEST --save --directory $LOG_DIR"
    "viewedgeprofiles -p 123314 -r 1 --separatix --wall --save --directory $LOG_DIR"
    "viewequilibrium -p 134174 -r 117 --rho -mdesc pf_active wall --save --directory $LOG_DIR"
    "viewfluxes -p 134174 -r  117 -m CLOSEST"
    "viewhcddistributions -p 130012 -r 115 -d TEST --save --directory $LOG_DIR"
    "viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3 --save --directory $LOG_DIR"
    "viewhcdwaves -p 134173 -r 101 -d TEST --save --directory $LOG_DIR"
    "viewkineticprofiles -p 134174 -r 117 --save --directory $LOG_DIR"
    "viewmachinedescription -mdesc wall pf_active --save --directory $LOG_DIR"
    "viewmachinedescription -mdesc wall --show-labels --save --directory $LOG_DIR"
    "viewneutron -p 121014 -r 11 -t 450 --save --directory $LOG_DIR"
    "viewplasmacompo -p 131047 -r 4"
    "viewpressure -p 134174 -r 117 --save --directory $LOG_DIR"
    "viewrotation -p 134174 -r 117 --save --directory $LOG_DIR"
    "viewscenario -p 134174 -r 117 --time 60 --save --directory $LOG_DIR"
    "viewscenario -p 134174 -r 117 --noProfiles --save --directory $LOG_DIR"
    "viewsources -p 134174 -r  117"
    "viewspectrometry -p 134000 -r 37 -d TEST --save --directory $LOG_DIR"
    "viewwall --save wall -m iter")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi
