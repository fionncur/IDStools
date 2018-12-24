#!/usr/bin/env python

from numpy.distutils.core import setup
import os

# Generate list of python scripts
here = os.path.abspath(os.path.dirname(__file__))
script_files = []
for file in os.listdir(os.path.join(here,'bin')):
    script_files.append(os.path.join(here,'bin',file))

setup(name='IMAS IDS Tools',
      version       = os.getenv("PKGVERSION"),
      description   = 'IMAS IDS Python tools',
      author        = "ITER Organization",
      author_email  = "imas-support@iter.org",
      url           = "https://imas.iter.org/",
      packages      = ['idstools'],
      py_modules    = [],
      scripts       = script_files,
     )
