#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools ()
from setuptools import setup

setup (name='CmtStandardNames',
       version='0.1.0',
       description='CSDMS standard names',
       author='Eric Hutton',
       author_email='eric.hutton@colorado.edu',
       url='https://csdms.colorado.edu',
       install_requires=['PyYAML'],
       packages=['standard_names', 'standard_names.tests'],
       entry_points = {
           'console_scripts': [
               'snbuild = standard_name.snbuild:main',
               'sndump = standard_name.sndump:main',
               'snscrape = standard_name.snscrape:main',
           ]
       },
       #scripts=['scripts/snbuild', 'scripts/sndump', 'scripts/snscrape'],
       package_data={'': ['data/*yaml']},
       test_suite='standard_names.tests',
      )
