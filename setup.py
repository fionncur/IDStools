#!/usr/bin/env python

from numpy.distutils.core import setup

setup(name='IMAS IDS Tools',
      version='1.0',
      description='IMAS IDS Python tools',
      packages=['idstools'],
      py_modules=[],
      scripts=['bin/imasdbs', 'bin/idsdiff', 'bin/idsdump', 'bin/idscopy']
     )
