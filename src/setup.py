#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools ()
from setuptools import setup

setup (name='CmtStandardNames',
       version='0.2.1',
       description='CSDMS standard names',
       author='Eric Hutton',
       author_email='eric.hutton@colorado.edu',
       url='https://csdms.colorado.edu',
       install_requires=['PyYAML'],
       packages=['standard_names', 'standard_names.cmd',
                 'standard_names.tests'],
       entry_points = {
           'console_scripts': [
               'snbuild = standard_names.cmd.snbuild:main',
               'sndump = standard_names.cmd.sndump:main',
               'snscrape = standard_names.cmd.snscrape:main',
           ]
       },
       package_data={'': ['data/*yaml']},
       test_suite='standard_names.tests',
      )
