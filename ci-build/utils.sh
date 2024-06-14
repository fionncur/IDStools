#!/bin/bash
##########################################################################################
#                              Common functions                                          #
##########################################################################################
getIMASModuleName() {
    # This function returns IMAS module name
    # example : getIMASModuleName intel-2020b
    local TOOLCHAIN_VERSION=$1
    local ACCESS_LAYER_VERSION=$2
    local DD_VERSION=$3
    if [ -z "$ACCESS_LAYER_VERSION" ]; then
        ACCESS_LAYER_VERSION="5"
    else
        ACCESS_LAYER_VERSION="$2"
    fi
    if [ -z "$DD_VERSION" ]; then
        DD_VERSION="3"
    else
        DD_VERSION="$3"
    fi
    #Semantic versioning
    IMASVERSIONSLIST=$(module av -t IMAS/ 2>&1 | grep -E "$DD_VERSION\.[0-9]+\.[0-9]+-$ACCESS_LAYER_VERSION\.[0-9]+\.[0-9]+-$TOOLCHAIN_VERSION")
    # CalVar versioning
    if [[ $ACCESS_LAYER_VERSION == "5" ]]; then
        IMASCALVERVERSIONSLIST=$(module av -t IMAS/ 2>&1 | grep -E "$DD_VERSION\.[0-9]+\.[0-9]+-[0-9]+\.[0-9]+-$TOOLCHAIN_VERSION")
    fi
    if [[ $TOOLCHAIN_VERSION == *"intel"* ]]; then
        IMAS_MODULE_VERSION=$(echo "$IMASVERSIONSLIST"$'\n'"$IMASCALVERVERSIONSLIST" | grep "intel" | sort -rV | head -n 1)
    fi
    if [[ $TOOLCHAIN_VERSION == *"foss"* ]]; then
        IMAS_MODULE_VERSION=$(echo "$IMASVERSIONSLIST"$'\n'"$IMASCALVERVERSIONSLIST" | grep "foss" | sort -rV | head -n 1)
    fi
    echo "$IMAS_MODULE_VERSION" | sed 's/(.*//'
}

# module use /work/imas/etc/modules/all
# module use -p /work/imas/opt/bamboo_deploy/easybuild/modules/all
# TEST
# toolchain=intel-2023b
# # getIMASModuleName $toolchain 4
# getIMASModuleName $toolchain 5
# getIMASModuleName $toolchain 5 3
