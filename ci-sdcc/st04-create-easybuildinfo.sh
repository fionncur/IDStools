#!/bin/bash
# Bamboo CI script to create build information for easybuild
# Execute script from root directory

source ./ci-sdcc/st00-header.sh $1 $2

# if successuful create hash and store in actor directory
COMMITHASH=$(git rev-parse HEAD)
VERSION=$(git describe --tags --always)
rm -f ./ci-sdcc/versioninfo.txt
cat >>./ci-sdcc/versioninfo.txt <<EOF
COMMITHASH=$COMMITHASH
MODULE_VERSION=$VERSION
IMAS_VERSION=$IMAS_VERSION
AL_VERSION=$AL_VERSION
TOOLCHAIN_VERSION=$TOOLCHAIN_VERSION
RUNMODULES=${RUNMODULES[@]}
EBRUNMODULES=${EBBRUNMODULES[@]}
EOF

cat ./ci-sdcc/versioninfo.txt

# Create ci acrtifact
tar -cvzf ci-sdcc.tar.gz ci-sdcc inputs >/dev/null 2>&1

# show contents of artifact
tar -tzvf ci-sdcc.tar.gz

echo "Done"
