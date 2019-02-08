#!/usr/bin/env python

from setuptools import setup
import os,glob
import subprocess

# Generate list of python scripts
script_files = glob.glob("bin/*")

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
      packages      = ['idstools'],
      py_modules    = [],
      scripts       = script_files,
     )
