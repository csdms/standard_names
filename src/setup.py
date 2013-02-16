from ez_setup import use_setuptools

use_setuptools ()

from setuptools import setup, find_packages

setup (name='standard_names',
       version='0.1',
       description='CSDMS standard names',
       author='Eric Hutton',
       author_email='eric.hutton@colorado.edu',
       url='https://csdms.colorado.edu',
       install_requires=['PyYAML'],
       packages=['standard_names'],
       scripts=['scripts/snbuild', 'scripts/sndump', 'scripts/snscrape'],
       package_data={'': ['data/*yaml']},
      )

