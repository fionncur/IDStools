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

SCRIPTS=(
"viewcoresources -s 130012 -r 105 -d TEST  --save"
"viewcoretransport -s 92436 -r 850  -d TEST --save" 
"vieweccomposition -s 134173 -r 2326 -d TEST --save" 
"viewecray -s 134173 -r 2326 -d TEST --save" 
"viewedgeprofiles -s 123314 -r 1 --separatix --wall --save"
"viewequilibrium -s 134174 -r 117 --rho --pfcoils --save"
"viewfluxes -s 134174 -r  117 -m CLOSEST"
"viewhcddistributions -s 130012 -r 115 -d TEST --save" 
"viewhcdplots -ech 134173/101/public/MDSPLUS/TEST/3 -nbi 130012/115/public/MDSPLUS/TEST/3 -fus 130012/115/public/MDSPLUS/TEST/3 -icrh 130012/15/public/MDSPLUS/TEST/3 --save"
"viewhcdwaves -s 134173 -r 101 -d TEST --save"
"viewkineticprofiles -s 134174 -r 117 --save"
"viewmachinedescription plot wall pf_active --save"
"viewmachinedescription list pf_active --checkValidity" 
"viewmachinedescription list pf_active --obsolete" 
"viewmachinedescription plot wall --save" 
"viewneutron -s 121014 -r 11 -t 450 --save"
"viewplasmacompo -s 131047 -r 4"
"viewpressure -s 134174 -r 117 --save"
"viewrotation -s 134174 -r 117 --save"
"viewscenario -s 134174 -r 117 --time 60 --save" 
"viewscenario -s 134174 -r 117 --noProfiles --save" 
"viewsources -s 134174 -r  117" 
"viewspectrometry -s 134000 -r 37 -d TEST --save" 
"viewwall --save wall iter")


execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    exit "$STATUS"
fi



