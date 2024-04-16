#!/bin/bash
# Bamboo test execution script for analysis scripts
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
# "viewedgeprofiles -s 123314 -r 1 --separatix --wall --save"
# 15-Apr-2024 17:31:03	./tests/st00_common.sh: line 19: 1898494 Illegal instruction     (core dumped) viewedgeprofiles -s 123314 -r 1 --separatix --wall --save

# "viewall database --uri \"imas:mdsplus?user=schneim;shot=92436;run=271;database=jet;version=3\""
SCRIPTS=(
"viewcoresources --uri \"imas:mdsplus?user=public;shot=130012;run=105;database=TEST;version=3\" --save" 
"viewcoretransport --uri \"imas:mdsplus?user=public;shot=92436;run=850;database=TEST;version=3\" --save" 
"vieweccomposition --uri \"imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3\" --save" 
"viewecray --uri \"imas:mdsplus?user=public;shot=134173;run=2326;database=TEST;version=3\" --save" 
"viewedgeprofiles --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --separatix --wall --time 60 --save" 
"viewequilibrium --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save" 
"viewfluxes --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" -m CLOSEST" 
"viewhcddistributions --uri \"imas:mdsplus?user=public;shot=130012;run=115;database=TEST;version=3\" --save" 
"viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3 --save" 
"viewhcdwaves --uri \"imas:mdsplus?user=public;shot=134173;run=101;database=TEST;version=3\" --save" 
"viewkineticprofiles --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save" 
"viewmachinedescription plot wall pf_active --save" 
"viewmachinedescription list pf_active --checkValidity" 
"viewmachinedescription list pf_active --obsolete"  
"viewmachinedescription plot wall --save"  
"viewneutron --uri \"imas:mdsplus?user=public;shot=121014;run=11;database=ITER;version=3\" -t 450 --save" 
"viewplasmacompo --uri \"imas:mdsplus?user=public;shot=131047;run=4;database=ITER;version=3\"" 
"viewpressure --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save" 
"viewrotation --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --save" 
"viewscenario --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --time 60 --save" 
"viewscenario --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" --noProfiles --save" 
"viewsources --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\"" 
"viewspectrometry --uri \"imas:mdsplus?user=public;shot=134000;run=37;database=TEST;version=3\" --save" 
"viewwall --save wall iter")


execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi



