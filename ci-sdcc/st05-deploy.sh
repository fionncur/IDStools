#!/bin/bash
# Bamboo deploy script using Easybuild
# Execute script from root directory

source ./ci-sdcc/utils.sh

# expand aliases
shopt -s expand_aliases

#print hostname
hostname -f

# Note Disable set -e option when using on local as it will exit the shell on error
if [[ "$(uname -n)" == *"bamboo"* ]]; then
    set -e -o pipefail
fi

MODULE_NAME_LOWER=IDStools
# upper case
MODULE_NAME=$MODULE_NAME_LOWER
################################################################################################
#                        Prepare Easybuild Modulefile                                          #
################################################################################################
VERSION_FILE="./ci-sdcc/versioninfo.txt"
echo "--------------------------------------"
echo "VERSION_FILE Contents: "
# Ensure version file is present and print contents of versioninfo.txt
cat $VERSION_FILE
echo "--------------------------------------"

# Get commit hash
COMMITHASH=$(awk -F "=" '/COMMITHASH/ {print $2}' $VERSION_FILE)
IMAS_VERSION=$(awk -F "=" '/IMAS_VERSION/ {print $2}' $VERSION_FILE)
AL_VERSION=$(awk -F "=" '/AL_VERSION/ {print $2}' $VERSION_FILE)
TOOLCHAIN_VERSION=$(awk -F "=" '/TOOLCHAIN_VERSION/ {print $2}' $VERSION_FILE)

EBRUNMODULES=$(awk -F "=" '/EBRUNMODULES/ {print $2}' $VERSION_FILE)

# Get raw version
RAWVERSION=$(awk -F "=" '/MODULE_VERSION/ {print $2}' $VERSION_FILE)

MODULE_VERSION=$RAWVERSION
if [[ $RAWVERSION == *-* ]]; then
    MODULE_VERSION=dev
fi

# For "never released" repositories git describe provies only comit hash
if [[ ! $RAWVERSION == *"."* ]]; then
    MODULE_VERSION=dev
fi
echo "--------------------------------------"
echo "Module version details : "
echo "COMMITHASH : $COMMITHASH"
echo "RAWVERSION : $RAWVERSION"
echo "MODULE_VERSION : $MODULE_VERSION"
echo "IMAS_VERSION : $IMAS_VERSION"
echo "AL_VERSION : $AL_VERSION"
echo "TOOLCHAIN_VERSION : $TOOLCHAIN_VERSION"
echo "EBRUNMODULES : $EBRUNMODULES"

# Creating module"
IFS='-' read -r TNAME TVERSION <<<"$TOOLCHAIN_VERSION"

MODULE_FULL_VERSION=$MODULE_NAME-$MODULE_VERSION-$TNAME-$TVERSION.eb

echo "$MODULE_FULL_VERSION"
echo "--------------------------------------"
sed -e "s;__COMMITHASH__;${COMMITHASH};" \
    -e "s;__VERSION__;${MODULE_VERSION};" \
    -e "s;__RAWVERSION__;${RAWVERSION};" \
    -e "s;__IMAS_VERSION__;${IMAS_VERSION};" \
    -e "s;__AL_VERSION__;${AL_VERSION};" \
    -e "s;__TOOLCHAIN_NAME__;${TNAME};" \
    -e "s;__TOOLCHAIN_VERSION__;${TVERSION};" \
    -e "s;__EBRUN_MODULES__;${EBRUNMODULES};" \
    ./ci-sdcc/ebfiles/"$MODULE_NAME".eb.in >./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION"

#format eb file
python3 -m venv build_venv && source build_venv/bin/activate && pip install --upgrade pip && pip install black && black ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" && deactivate
rm -rf build_venv
# create eb tar file
tar -cvzf eb.tar.gz ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" >/dev/null 2>&1

################################################################################################
#                                   Easybuild                                                  #
################################################################################################

# Set up environment for compilation
if [ -z "$DEPLOY_DIRECTORY" ]; then
    if [[ "$(uname -n)" != "sdcc"* ]]; then
        DEPLOY_DIRECTORY="/mnt/bamboo_deploy"
    else
        DEPLOY_DIRECTORY=$(pwd)
        # Provide Git Token when running on local
        if [ -z "$bamboo_HTTP_AUTH_BEARER_PASSWORD" ]; then
            bamboo_HTTP_AUTH_BEARER_PASSWORD=
        fi
    fi
fi

# contents of eb file
echo "----------------------------------------------------"
cat ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION"
echo "----------------------------------------------------"
# Load modules

echo "Loading Modules"
source /etc/profile.d/modules.sh
module purge
module load EasyBuild
echo "Done loading modules..."

EASYBUILD_DIR="$DEPLOY_DIRECTORY/easybuild"

# create directory EASYBUILD_DIR if not exists"
mkdir -p "$EASYBUILD_DIR"

# prepare HTTP auth file
EB_HTTP_OPTS=$(writeGitHeaderFile "$bamboo_HTTP_AUTH_BEARER_PASSWORD")
# prepare EB options
EB_OPTS=(
    --force
    --force-download
    "--modules-tool=Lmod"
    --module-syntax=Tcl
    --allow-modules-tool-mismatch
    --allow-use-as-root-and-accept-consequences
    "--prefix=$EASYBUILD_DIR"
    "--optarch=Intel:-axAVX,-CORE-AVX2;GCC:march=sandybridge"
    "$EB_HTTP_OPTS"
)
# enable if need to debug --logtostdout --debug --trace
EB_OPTS=(${EB_OPTS[@]})

#Check contents of the paths
if [ -d "$EASYBUILD_DIR"/sources/"${MODULE_NAME_LOWER:0:1}"/"$MODULE_NAME" ]; then
    ls "$EASYBUILD_DIR"/sources/"${MODULE_NAME_LOWER:0:1}"/"$MODULE_NAME"
fi
if [ -d "$EASYBUILD_DIR"/software/"$MODULE_NAME" ]; then
    ls "$EASYBUILD_DIR"/software/"$MODULE_NAME"
fi

echo "=============================================================================="
echo "> Injecting checksum"

eb ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" --inject-checksums ${EB_OPTS[@]}

echo "=============================================================================="
#echo "> Checking style"
#$EB_INSTALLPYTHON -m venv stylevenv && source ./stylevenv/bin/activate && pip install -- pycodestyle && eb ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" ${EB_OPTS[@]} --check-style && deactivate
#rm -rf stylevenv
# eb ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" --check-style ${EB_OPTS[@]}

echo "=============================================================================="
echo "> execute eb"
eb ./ci-sdcc/ebfiles/"$MODULE_FULL_VERSION" ${EB_OPTS[@]}


if [ $? -eq 0 ]; then
    echo "$MODULE_FULL_VERSION is installed"
else
    echo "$MODULE_FULL_VERSION is not installed"
fi
# Replace mnt with /work/imas/opt/ to work internal path on sdcc"
if [[ "$(uname -n)" != "sdcc"* ]]; then
    find "$EASYBUILD_DIR"/modules/all/"$MODULE_NAME" -type f -not -path '*/\.*' -exec sed -i -- 's/mnt/work\/imas\/opt/g' {} +
    find "$EASYBUILD_DIR"/modules/data/"$MODULE_NAME" -type f -not -path '*/\.*' -exec sed -i -- 's/mnt/work\/imas\/opt/g' {} +
fi

# Check available module"
if [[ "$(uname -n)" != "sdcc"* ]]; then
    module use -p /work/imas/opt/bamboo_deploy/easybuild/modules/all
else
    module use -p "$EASYBUILD_DIR"/modules/all
fi
module -r -t avail "$MODULE_NAME"/

deleteGitHeaderFile
echo "Done"
