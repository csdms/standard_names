#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools ()
from setuptools import setup

setup (name='CmtStandardNames',
       version='0.1.2',
       description='CSDMS standard names',
       author='Eric Hutton',
       author_email='eric.hutton@colorado.edu',
       url='https://csdms.colorado.edu',
       install_requires=['PyYAML'],
       namespace_packages=['cmt'],
       packages=['cmt', 'cmt.standard_names', 'cmt.standard_names.tests'],
       entry_points = {
           'console_scripts': [
               'snbuild = cmt.standard_names.snbuild:main',
               'sndump = cmt.standard_names.sndump:main',
               'snscrape = cmt.standard_names.snscrape:main',
           ]
       },
       package_data={'': ['data/*yaml']},
       test_suite='cmt.standard_names.tests',
      )
