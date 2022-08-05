#!/usr/bin/env python

from setuptools import setup
import os,glob
import subprocess

# Generate list of python scripts
script_files = glob.glob("bin/*")
script_files.append("database_tools/ids_shift_eq.py")
script_files.append("database_tools/ids_rescale_eq.py")
script_files.append("database_tools/rosettacode.py")
script_files.append("idstools/idsdef.py")


# Get version by PKGVERSION, .version file, or git describe
def get_version():
    version = os.getenv("PKGVERSION")
    if not version and os.path.isfile('.version'):
        version = open(".version").read()
    if not version and os.path.isdir('.git'):
        version = subprocess.check_output(["git", "describe"]).strip().decode('ascii')
        if '-' in version:
            p = version.split('-')
            version = p[0]+'.dev'+p[1]+'+'+''.join(p[2:])
    return version

setup(name='IMAS IDS Tools',
      version       = get_version(),
      description   = 'IMAS IDS Python tools',
      author        = "ITER Organization",
      author_email  = "imas-support@iter.org",
      url           = "https://imas.iter.org/",
      packages      = ['idstools','database_tools'],
      py_modules    = [],
      scripts       = script_files,
      data_files    = [('bin/mappings',['database_tools/mappings/h-mode-db-mapping.csv'])]
     )
