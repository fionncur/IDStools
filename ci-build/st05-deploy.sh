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

EB_OPTS="--modules-tool=EnvironmentModules --module-syntax=Tcl --allow-modules-tool-mismatch --allow-use-as-root-and-accept-consequences --prefix=/mnt/bamboo_deploy/easybuild"
write_headers_file

set -e
set -v
MODULE_NAME=IDSTools
COMMITHASH=$(awk -F "=" '/COMMITHASH/ {print $2}' ./ci-build/versioninfo.txt)
VERSION=$(awk -F "=" '/VERSION/ {print $2}' ./ci-build/versioninfo.txt)
TOOLCHAIN_NAME=foss
TOOLCHAIN_VERSION=2020b
MODULE_FULL_VERSION=$MODULE_NAME-$VERSION-$TOOLCHAIN_NAME-$TOOLCHAIN_VERSION.eb

echo "COMMITHASH :" $COMMITHASH
echo "VERSION :" $VERSION
echo "MODULE_FULL_VERSION :" $MODULE_FULL_VERSION

sed -e 's;__COMMITHASH__;$COMMITHASH;'\
    -e 's;__VERSION__;$VERSION;' \
    -e 's;__TOOLCHAIN_NAME__;$TOOLCHAIN_NAME;' \
    -e 's;__TOOLCHAIN_VERSION__;$TOOLCHAIN_VERSION;' \
    ./ci-build/files/idstools.eb.in > ./ci-build/files/$MODULE_FULL_VERSION

echo "content of eb file"
cat ./ci-build/files/$MODULE_FULL_VERSION
eb ./ci-build/files/$MODULE_FULL_VERSION -f ${EB_OPTS} ${EB_HTTP_OPTS}

del_headers_file