#!/bin/bash
# Bamboo script
# Stage 2 : Unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

tar xvf ${PREFIX_DIR}.tar.gz 

python3 -m venv build_venv
source build_venv/bin/activate
python3 -c 'import sys; print("Python version in virtual env : %d.%d"% sys.version_info[0:2])'

pip3 install --upgrade pip
pip3 install -r requirements.txt
array=( dist/*.whl )
echo "${arrray[0]}"

pip3 install dist/${arrray[0]} --upgrade
pip list

chmod +x ./tests/testscripts.sh
try bash ./tests/testscripts.sh

pytest tests 


deactivate
try rm -r build_venv


