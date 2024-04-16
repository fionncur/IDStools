#!/bin/bash
# Bamboo test execution script for ids manipulation scripts
# Execute script from root directory
source ./tests/st00_common.sh
# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

#Get user name
USERNAME=$(whoami)

# create log directory
LOG_DIR=$PWD/"logs"
rm -rf "$LOG_DIR"
mkdir -p "$LOG_DIR"


SCRIPTS=(
"eqdsk2ids --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" -g resources/geqdsk/example.gfile -u $USERNAME -d ITER --log INFO" 
"idschk --uri \"imas:mdsplus?user=public;shot=134174;run=117;database=ITER;version=3\" -f resources/validation_schemas/generic/core_profiles.yml" 
"idscp --input_uri \"imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3\" --output_uri \"imas:mdsplus?user=$USERNAME;shot=145000;run=2;database=ITER;version=3\"" 
"idsdiff --uriA \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" --uriB \"imas:mdsplus?user=public;shot=122525;run=2;database=ITER;version=3\" summary" 
"idsdiff --uriA \"imas:mdsplus?user=public;shot=130011;run=6;database=ITER;version=3\" --uriB \"imas:mdsplus?user=public;shot=130012;run=4;database=ITER;version=3\" summary" 
"idsresample --input_uri \"imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3\" --output_uri \"imas:mdsplus?user=$USERNAME;shot=131024;run=2;database=ITER;version=3\"" 
"idsrescale_equilibrium --input_uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" --output_uri \"imas:mdsplus?user=$USERNAME;shot=122222;run=22;database=ITER;version=3\"  --rescale 2" 
"idsshift_equilibrium --input_uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" --output_uri \"imas:mdsplus?user=$USERNAME;shot=123001;run=1;database=ITER;version=3\"  --shift -0.01" 
"idslist --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\"" 
"idslist --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" yaml" 
"idslist --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" occ" 
"idsperf --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" summary" 
"idsperf --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" summary --verbose --outputRun 5 --showStats --repeat 2" 
"idsperf --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" summary --verbose --outputRun 5 --showStats --repeat 2 --uriOut \"imas:mdsplus?user=$USERNAME;shot=131024;run=20;database=ITER;version=3\" --memoryBackend" 
"idsprint --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" equilibrium" 
"idssize --uri \"imas:mdsplus?user=public;shot=122525;run=1;database=ITER;version=3\" equilibrium" 
"idssize --uri \"imas:mdsplus?user=public;shot=131024;run=10;database=ITER;version=3\"")

execute_scripts "${SCRIPTS[@]}"
STATUS=$?
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    if [ "$STATUS" -ne 0 ]; then
        exit "$STATUS"
    fi
fi


