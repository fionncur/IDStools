#!/bin/bash
source /etc/profile.d/modules.sh
source ./ci-sdcc/utils.sh
##########################################################################################
#                     Set environment based on toolchain                                 #
##########################################################################################

module use /work/imas/etc/modules/all

module purge

# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# Get toolchain version
if [ -z "$1" ]; then
    TOOLCHAIN_VERSION="intel-2023b"
else
    TOOLCHAIN_VERSION="$1"
fi

# Get AL version
if [ -z "$2" ]; then
    ACCESS_LAYER_VERSION="5"
else
    ACCESS_LAYER_VERSION="$2"
fi

echo "Building for $TOOLCHAIN_VERSION and Access Layer $ACCESS_LAYER_VERSION"

if [[ $TOOLCHAIN_VERSION == *"intel"* ]]; then
    FCOMPILER="ifort"
fi
if [[ $TOOLCHAIN_VERSION == *"foss"* ]]; then
    FCOMPILER="gfortran"
fi

IMAS_MODULE_VERSION=$(getIMASModuleName "$TOOLCHAIN_VERSION" "$ACCESS_LAYER_VERSION")
# load IMAS module first
module load "$IMAS_MODULE_VERSION"

GCCcore_VERSION=$(getGCCcoreVersion)
module unload "$IMAS_MODULE_VERSION"
dependencies="./ci-sdcc/dependencies.txt"

# Check if the file exists
if [ ! -f "$dependencies" ]; then
    echo "File $dependencies not found."
    exit 1
fi

declare -a RUNMODULES=()
declare -a EBBRUNMODULES=()

# actors have version suffix so better to provide them as EXTERNAL_MODULE

counter=0
# Read the file line by line
while IFS= read -r line || [[ -n $line ]]; do
    # for empty string continue
    if [[ -z "${line// /}" ]]; then
        counter=$(("$counter" + 1))
        continue
    fi
    # latest module version as it is not given
    if [[ $line == "IMAS" ]]; then
        echo "Using latest version of IMAS $IMAS_MODULE_VERSION"
        RUNMODULES["$counter"]="$IMAS_MODULE_VERSION"
        EBBRUNMODULES["$counter"]="('$IMAS_MODULE_VERSION', EXTERNAL_MODULE),"
    else
        module_version=$(getModuleName "$line" "$TOOLCHAIN_VERSION" "$GCCcore_VERSION")
        echo "Using latest version of $line $module_version"
        RUNMODULES["$counter"]="$module_version"
        EBBRUNMODULES["$counter"]=$(getModuleNameAndVersion "$module_version")

    fi
    counter=$(("$counter" + 1))
done <"$dependencies"

echo "TOOLCHAIN_VERSION : $TOOLCHAIN_VERSION"
echo "GCCcore_VERSION : $GCCcore_VERSION"
echo "IMAS VERSION : $IMAS_MODULE_VERSION"
echo "BUILDMODULES : " "${BUILDMODULES[@]}"
echo "RUNMODULES : " "${RUNMODULES[@]}"
echo "EBRUNMODULES : " "${EBBRUNMODULES[@]}"
echo "Compiler : $FCOMPILER"

echo "Loading modules..."
module purge
module load "${RUNMODULES[@]}"
echo "Done loading modules..."
