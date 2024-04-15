#!/bin/bash
##########################################################################################
#                              Common functions                                          #
##########################################################################################
getIMASModuleName() {
    # This function retturns IMAS module name
    # example : getIMASModuleName intel-2020b
    local TOOLCHAIN_VERSION=$1
    local ACCESS_LAYER_VERSION=$2

    if [ -z "$ACCESS_LAYER_VERSION" ]; then
        ACCESS_LAYER_VERSION="4"
    else
        ACCESS_LAYER_VERSION="$2"
    fi
    IMASVERSIONSLIST=$(module av -t IMAS/ 2>&1 | grep "3.*.*-$ACCESS_LAYER_VERSION.*.*-$TOOLCHAIN_VERSION")

    if [[ $TOOLCHAIN_VERSION == *"intel"* ]]; then
        IMAS_MODULE_VERSION=$(echo "$IMASVERSIONSLIST" | grep "intel" | sort -rV | head -n 1)
    fi
    if [[ $TOOLCHAIN_VERSION == *"foss"* ]]; then
        IMAS_MODULE_VERSION=$(echo "$IMASVERSIONSLIST" | grep "foss" | sort -rV | head -n 1)
    fi
    echo "${IMAS_MODULE_VERSION//(default)/}"
}
