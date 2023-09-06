#!/bin/bash
rm -rf build_venv
python -m venv build_venv

. build_venv/bin/activate
python --version
pip install --upgrade pip
pip install -r docs/requirements.txt
pip list

# Build documentation
cd docs
make realclean
make man
cd ..
deactivate
rm -rf build_venv