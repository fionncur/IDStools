#!/bin/bash
# Bamboo Build script
# Stage 0 : load modules

# Set up environment for compilation
. /usr/share/Modules/init/sh
module use /work/imas/etc/modules/all
module purge
module load EasyBuild

HTTPHEADERS=http-headers.txt

write_headers_file() {
# Taken from https://git.iter.org/projects/IMEX/repos/easybuild-easyconfigs/pull-requests/121/diff
# EB v4.3.3 supports --http-header-fields-urlpat=FILE, construct a file for
# git.iter.org url patterns (makes CI MAGIC:http_auth_hooks.sh unnecessary)
# but to avoid exposure of the hash to the CI logs, use a PASSWORD variable.
# Also delete the file after use.
rm -rf "$HTTPHEADERS"  # Start anew
# Preformatted header for use with access tokens on git.iter.org
if [ "x$bamboo_HTTP_AUTH_BEARER_PASSWORD" != "x" ]; then
    cat >> $HTTPHEADERS <<EOF
iter.org::Authorization: Bearer $bamboo_HTTP_AUTH_BEARER_PASSWORD
EOF
    EB_HTTP_OPTS="--http-header-fields-urlpat=${HTTPHEADERS}"
fi

# Add one custom HTTP HEADER line at a time (urlpat::header_field)
# Expose the value of urlpat, but not the header_field, this allows later
# line-by-line maintenance in the CI build plan variables.
# for N in {1..9} ;do
#     var_urlpat=bamboo_HTTP_HEADER_URLPAT_${N}
#     var_field=bamboo_HTTP_HEADER_URLPAT_${N}_PASSWORD
#     if test "x${!var_urlpat}" != "x" -a "x${!var_field}" != "x" ;then
#         cat >> $HTTPHEADERS <<EOF
# ${!var_urlpat}::${!var_field}
# EOF
#     fi
# done
}

del_headers_file() {
if [ -e ${HTTPHEADERS} ]; then
    rm ${HTTPHEADERS}
fi
}

echo "listing contents of current directory"
ls

echo "listing contents of :" /mnt/bamboo_deploy
ls /mnt/bamboo_deploy
echo "----------------------------------------------------------"

echo "creating directory :/mnt/bamboo_deploy/easybuild" 
mkdir -p /mnt/bamboo_deploy/easybuild || exit 1
echo "----------------------------------------------------------"

chmod -R u+w /mnt/bamboo_deploy/easybuild
# rm -rf /mnt/bamboo_deploy/easybuild
EB_OPTS="--modules-tool=EnvironmentModules --module-syntax=Tcl --allow-modules-tool-mismatch --allow-use-as-root-and-accept-consequences --prefix=/mnt/bamboo_deploy/easybuild"
write_headers_file

set -e
set -v

echo "Contents of versioninfo.txt"
cat ./ci-build/versioninfo.txt

MODULE_NAME=IDSTools
COMMITHASH=$(awk -F "=" '/COMMITHASH/ {print $2}' ./ci-build/versioninfo.txt)
RAWVERSION=$(awk -F "=" '/VERSION/ {print $2}' ./ci-build/versioninfo.txt)
VERSION=$RAWVERSION
if [[ $RAWVERSION == *-* ]]; then
    VERSION=dev
fi

echo "COMMITHASH :" $COMMITHASH
echo "VERSION :" $VERSION

echo "creating foss-2020b module"
TOOLCHAIN_NAME=foss
TOOLCHAIN_VERSION=2020b
PYTHON_VERSION=3\\.8\\.6
SCIPY_VERSION=2020\\.11
MODULE_FULL_VERSION=$MODULE_NAME-$VERSION-$TOOLCHAIN_NAME-$TOOLCHAIN_VERSION.eb
echo "PYTHON_VERSION :" $PYTHON_VERSION
echo "SCIPY_VERSION :" $SCIPY_VERSION
echo "MODULE_FULL_VERSION :" $MODULE_FULL_VERSION

sed -e "s;__COMMITHASH__;${COMMITHASH};" \
    -e "s;__VERSION__;${VERSION};" \
    -e "s;__PYTHON_VERSION__;${PYTHON_VERSION};" \
    -e "s;__SCIPY_VERSION__;${SCIPY_VERSION};" \
    -e "s;__TOOLCHAIN_NAME__;${TOOLCHAIN_NAME};" \
    -e "s;__TOOLCHAIN_VERSION__;${TOOLCHAIN_VERSION};" \
    ./ci-build/files/idstools.eb.in > ./ci-build/files/$MODULE_FULL_VERSION

echo "contents of eb file" $MODULE_FULL_VERSION
echo "-----------------------START--------------------------------"
cat ./ci-build/files/$MODULE_FULL_VERSION
echo "-----------------------END----------------------------------"
eb ./ci-build/files/$MODULE_FULL_VERSION -f ${EB_OPTS} ${EB_HTTP_OPTS}
echo $MODULE_FULL_VERSION "Installed"

echo "creating gfbf-2022b module"
TOOLCHAIN_NAME=gfbf
TOOLCHAIN_VERSION=2022b
PYTHON_VERSION=3\\.10\\.8
SCIPY_VERSION=2023\\.02
MODULE_FULL_VERSION=$MODULE_NAME-$VERSION-$TOOLCHAIN_NAME-$TOOLCHAIN_VERSION.eb
echo "MODULE_FULL_VERSION :" $MODULE_FULL_VERSION

sed -e "s;__COMMITHASH__;${COMMITHASH};" \
    -e "s;__VERSION__;${VERSION};" \
    -e "s;__PYTHON_VERSION__;${PYTHON_VERSION};" \
    -e "s;__SCIPY_VERSION__;${SCIPY_VERSION};" \
    -e "s;__TOOLCHAIN_NAME__;${TOOLCHAIN_NAME};" \
    -e "s;__TOOLCHAIN_VERSION__;${TOOLCHAIN_VERSION};" \
    ./ci-build/files/idstools.eb.in > ./ci-build/files/$MODULE_FULL_VERSION

echo "contents of eb file" $MODULE_FULL_VERSION
echo "-----------------------START--------------------------------"
cat ./ci-build/files/$MODULE_FULL_VERSION
echo "-----------------------END----------------------------------"
eb ./ci-build/files/$MODULE_FULL_VERSION -f ${EB_OPTS} ${EB_HTTP_OPTS}
echo $MODULE_FULL_VERSION "Installed"

echo "creating intel-2020b module"
TOOLCHAIN_NAME=intel
TOOLCHAIN_VERSION=2020b
PYTHON_VERSION=3\\.8\\.6
SCIPY_VERSION=2020\\.11
MODULE_FULL_VERSION=$MODULE_NAME-$VERSION-$TOOLCHAIN_NAME-$TOOLCHAIN_VERSION.eb
echo "MODULE_FULL_VERSION :" $MODULE_FULL_VERSION

sed -e "s;__COMMITHASH__;${COMMITHASH};" \
    -e "s;__VERSION__;${VERSION};" \
    -e "s;__PYTHON_VERSION__;${PYTHON_VERSION};" \
    -e "s;__SCIPY_VERSION__;${SCIPY_VERSION};" \
    -e "s;__TOOLCHAIN_NAME__;${TOOLCHAIN_NAME};" \
    -e "s;__TOOLCHAIN_VERSION__;${TOOLCHAIN_VERSION};" \
    ./ci-build/files/idstools.eb.in > ./ci-build/files/$MODULE_FULL_VERSION

echo "contents of eb file" $MODULE_FULL_VERSION
echo "-----------------------START--------------------------------"
cat ./ci-build/files/$MODULE_FULL_VERSION
echo "-----------------------END----------------------------------"
eb ./ci-build/files/$MODULE_FULL_VERSION -f ${EB_OPTS} ${EB_HTTP_OPTS}
echo $MODULE_FULL_VERSION "Installed"

echo "check available idstools modules"
module use -p /work/imas/opt/bamboo_deploy/easybuild/modules/all
module avail -i idstools

del_headers_file