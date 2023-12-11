#!/usr/bin/env python
from setuptools import setup


setup(
    name="standard_names",
    version="0.2.7.dev0",
    description="CSDMS standard names",
    author="Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    url="https://csdms.colorado.edu",
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        "pyyaml",
        "six",
        "packaging",
        "jinja2",
        "py-scripting",
        "binaryornot",
    ],
    packages=[
        "standard_names",
        "standard_names.cmd",
        "standard_names.utilities",
        "standard_names.tests",
    ],
    entry_points={
        "console_scripts": [
            "snbuild = standard_names.cmd.snbuild:run",
            "sndump = standard_names.cmd.sndump:run",
            "snscrape = standard_names.cmd.snscrape:run",
            "snsql = standard_names.cmd.snsql:run",
            "snvalidate = standard_names.cmd.snvalidate:run",
        ]
    },
    package_data={"": ["data/*txt"]},
    test_suite="standard_names.tests",
)
