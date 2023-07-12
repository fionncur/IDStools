#!/bin/bash

# 3-fingered-claw 
function yell () 
{ 
  echo "$0: $*" >&2
}

function die () 
{ 
  yell "$*"; # exit 1
}

function try () 
{ 
  "$@" || die "cannot $*" 
}


# Default to foss toolchain
if [[ "$1" == "foss" || -z $1 ]];
then
    toolchain=foss
elif [[ "$1" == "intel" ]];
then
    toolchain=intel
fi
echo "Toolchain: $toolchain"

# Default to production config. 
if [[ "$2" == "prod" || -z $2 ]];
then
    config=prod
elif [[ "$2" == "dev" ]];
then
    config=dev
fi
echo "Configuration: $config"

# Testing/Coverage requirements
try module load coverage/5.5-GCCcore-10.2.0 

#IMAS Requirement
try module load IMAS
try module unload -f IDStools