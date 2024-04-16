#!/bin/bash
# Bamboo test execution script for analysis scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -p expand_aliases

#print hostname
hostname -f

# create log directory
LOG_DIR=$PWD/"logs"
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"
# "viewedgeprofiles -p 123314 -r 1 --separatix --wall --save"
# 15-Apr-2024 17:31:03	./tests/st00_common.sh: line 19: 1898494 Illegal instruction     (core dumped) viewedgeprofiles -p 123314 -r 1 --separatix --wall --save

SCRIPTS=(
"viewcoresources -p 130012 -r 105 -d TEST  --save"
"viewcoretransport -p 92436 -r 850  -d TEST --save" 
"vieweccomposition -p 134173 -r 2326 -d TEST --save" 
"viewecray -p 134173 -r 2326 -d TEST --save" 
"viewequilibrium -p 134174 -r 117 --rho --pfcoils --save"
"viewfluxes -p 134174 -r  117 -m CLOSEST"
"viewhcddistributions -p 130012 -r 115 -d TEST --save" 
"viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3 --save"
"viewhcdwaves -p 134173 -r 101 -d TEST --save"
"viewkineticprofiles -p 134174 -r 117 --save"
"viewmachinedescription plot wall pf_active --save"
"viewmachinedescription list pf_active --checkValidity" 
"viewmachinedescription list pf_active --obsolete" 
"viewmachinedescription plot wall --save" 
"viewneutron -p 121014 -r 11 -t 450 --save"
"viewplasmacompo -p 131047 -r 4"
"viewpressure -p 134174 -r 117 --save"
"viewrotation -p 134174 -r 117 --save"
"viewscenario -p 134174 -r 117 --time 60 --save" 
"viewscenario -p 134174 -r 117 --noProfiles --save" 
"viewsources -p 134174 -r  117" 
"viewspectrometry -p 134000 -r 37 -d TEST --save" 
"viewwall --save wall iter")


execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi



