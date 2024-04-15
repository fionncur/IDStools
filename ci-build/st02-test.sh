#!/bin/bash
# Bamboo script
# Stage 2 : Unit tests

# Set up environment
. ci-build/st00-header.sh $* || exit 1

# Unzip artifact
tar -xvzf ${PREFIX_DIR}.tar.gz ./${PREFIX_DIR}

try mkdir dependencies
python3 -m pip install --target=dependencies -r requirements.txt
export PYTHONPATH=$(get_abs_filename "./dependencies"):${PYTHONPATH}

# run tests
echo "Check environment for AL4"
export PYVERSION=$(python3 -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
echo "PYVERSION :" $PYVERSION
export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}")/lib/python${PYVERSION}/site-packages:${PYTHONPATH}
echo "PYTHONPATH :" $PYTHONPATH | grep -i idstools
export PATH=$(get_abs_filename "./${PREFIX_DIR}")/bin:${PATH}
echo "PATH :" $PATH | grep -i idstools

echo "Tools testing with testscripts with default IMAS Access Layer"
chmod +x ./tests/st01_test_ids_scripts.sh
chmod +x ./tests/st02_test_db_scripts.sh
chmod +x ./tests/st03_test_analysis_scripts.sh
try source ./tests/st01_test_ids_scripts.sh 
try source ./tests/st02_test_db_scripts.sh 
try source ./tests/st03_test_analysis_scripts.sh 


echo "-------------------------------------------------------------------------"
echo "Tools testing with testscripts with IMAS Access Layer 5"
try module purge
try module unload -f IMAS
try module load IMAS/3.41.0-4.11.10-foss-2023b
try module unload -f IDStools
echo module list | grep IMAS

echo "Check environment for AL5 2023b"
export PYVERSION=$(python3 -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
echo "PYVERSION :" $PYVERSION
export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}")/lib/python${PYVERSION}/site-packages:${PYTHONPATH}
echo "PYTHONPATH :" $PYTHONPATH | grep -i idstools
export PATH=$(get_abs_filename "./${PREFIX_DIR}")/bin:${PATH}
echo "PATH :" $PATH | grep -i idstools

try source ./tests/st01_test_ids_scripts.sh 
try source ./tests/st02_test_db_scripts.sh 
try source ./tests/st03_test_analysis_scripts.sh 

echo "-------------------------------------------------------------------------"
echo "Tools testing with testscripts with IMAS Access Layer 5"
try module purge
try module unload -f IMAS
try module load IMAS/3.40.1-5.1.0-foss-2020b
try module unload -f IDStools
echo module list | grep IMAS

echo "Check environment for AL5"
export PYVERSION=$(python3 -c 'import sys; print("%d.%d"% sys.version_info[0:2])')
echo "PYVERSION :" $PYVERSION
export PYTHONPATH=$(get_abs_filename "./${PREFIX_DIR}")/lib/python${PYVERSION}/site-packages:${PYTHONPATH}
echo "PYTHONPATH :" $PYTHONPATH | grep -i idstools
export PATH=$(get_abs_filename "./${PREFIX_DIR}")/bin:${PATH}
echo "PATH :" $PATH | grep -i idstools

try source ./tests/st01_test_ids_scripts.sh 
try source ./tests/st02_test_db_scripts.sh 
try source ./tests/st03_test_analysis_scripts.sh 

echo "Run pytest for functions testing"
try python3 -m pytest --junit-xml=${PREFIX_DIR}/test_report.xml tests || exit 1
