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

# "viewall database --uri \"imas:mdsplus?user=schneim;shot=92436;run=271;database=jet;version=3\""
SCRIPTS=(
"viewcoresources --uri \"imas:mdsplus?user=public;shot=130012;run=105;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewcoretransport --uri \"imas:mdsplus?user=public;shot=92436;run=850;database=TEST;version=3\" --save --directory $LOG_DIR" 
"vieweccomposition --uri \"imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewecray --uri \"imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewedgeprofiles --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --separatix --wall --time 60 --save --directory $LOG_DIR" 
"viewequilibrium --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" pf_active wall --save --directory $LOG_DIR"
"viewfluxes --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" -m CLOSEST" 
"viewhcddistributions --uri \"imas:mdsplus?user=public;shot=130012;run=115;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3 --save --directory $LOG_DIR" 
"viewhcdwaves --uri \"imas:mdsplus?user=public;shot=134173;run=101;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewkineticprofiles --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save --directory $LOG_DIR" 
"viewkineticprofiles --uri \"imas:mdsplus?path=/work/imas/shared/imasdb/ITER/3/134174/117\" --save --directory $LOG_DIR" 
"viewmachinedescription plot wall pf_active --save --directory $LOG_DIR" 
"viewmachinedescription list pf_active --checkValidity" 
"viewmachinedescription list pf_active --obsolete"  
"viewmachinedescription plot wall --save --directory $LOG_DIR"  
"viewneutron --uri \"imas:mdsplus?user=public;shot=121014;run=11;database=ITER;version=3\" -t 450 --save --directory $LOG_DIR" 
"viewplasmacompo --uri \"imas:mdsplus?user=public;shot=131047;run=4;database=ITER;version=3\"" 
"viewpressure --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save --directory $LOG_DIR" 
"viewpressure --uri \"imas:mdsplus?path=/work/imas/shared/imasdb/ITER/3/134174/117\" --save --directory $LOG_DIR" 
"viewrotation --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save --directory $LOG_DIR" 
"viewscenario --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --time 60 --save --directory $LOG_DIR" 
"viewscenario --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --noProfiles --save --directory $LOG_DIR" 
"viewsources --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\"" 
"viewspectrometry --uri \"imas:mdsplus?user=public;shot=134000;run=37;database=TEST;version=3\" --save --directory $LOG_DIR" 
"viewspectrometry -uri \"imas:mdsplus?path=/work/imas/shared/imasdb/TEST/3/134000/37\" --save --directory $LOG_DIR" 
"viewwall --save wall iter")


execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi



