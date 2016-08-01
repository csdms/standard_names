#!/usr/bin/env python


from setuptools import setup


setup (name='standard_names',
       version='0.2.2',
       description='CSDMS standard names',
       author='Eric Hutton',
       author_email='eric.hutton@colorado.edu',
       url='https://csdms.colorado.edu',
       install_requires=['pyyaml'],
       packages=['standard_names', 'standard_names.cmd',
                 'standard_names.utilities', 'standard_names.tests'],
       entry_points = {
           'console_scripts': [
               'snbuild = standard_names.cmd.snbuild:main',
               'sndump = standard_names.cmd.sndump:main',
               'snscrape = standard_names.cmd.snscrape:main',
               'snsql = standard_names.cmd.snsql:main',
               'snvalidate = standard_names.cmd.snvalidate:main',
           ]
       },
       package_data={'': ['data/*txt']},
       test_suite='standard_names.tests',
      )
