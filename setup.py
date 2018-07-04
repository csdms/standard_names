#!/usr/bin/env python


from setuptools import setup

import versioneer


setup(
    name="standard_names",
    version=versioneer.get_version(),
    description="CSDMS standard names",
    author="Eric Hutton",
    author_email="eric.hutton@colorado.edu",
    url="https://csdms.colorado.edu",
    install_requires=["pyyaml"],
    packages=[
        "standard_names",
        "standard_names.cmd",
        "standard_names.utilities",
        "standard_names.tests",
    ],
    cmdclass=versioneer.get_cmdclass(),
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
