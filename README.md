[![Test](https://github.com/csdms/standard_names/actions/workflows/test.yml/badge.svg)](https://github.com/csdms/standard_names/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/standard-names/badge/?version=latest)](http://standard-names.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/csdms/standard_names/badge.svg?branch=master)](https://coveralls.io/github/csdms/standard_names?branch=master)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/standard_names.svg)](https://anaconda.org/conda-forge/standard_names)
[![PyPI](https://img.shields.io/pypi/v/standard_names)](https://pypi.org/project/standard_names)


# standard_names

Python utilities for working with CSDMS Standard Names.

CSDMS Standard Names is an element of the [CSDMS Workbench](https://csdms.colorado.edu/wiki/Workbench),
an integrated system of software tools, technologies, and standards
for building and coupling models.

## As Regular Expression

```
^                           # Start of the object name
[a-z]+                      # Starts with one or more lowercase letters
(?:                         # Start of a non-capturing group for subsequent parts
    [-~_]?                  # Optional separator: hyphen, tilde, or underscore
    [a-zA-Z0-9]+            # One or more alphanumeric characters
)*                          # Zero or more repetitions of the group
__                          # Double underscore separator
[a-z]+                      # Start of the quantity
(?:                         # Start of a non-capturing group for subsequent parts
    [-~_]?                  # Optional separator: hyphen, tilde, or underscore
    [a-zA-Z0-9]+            # One or more alphanumeric characters
)*                          # Zero or more repetitions of the group
$                           # End of the name
```

## As Parsing Expression Grammar

```peg
Start
    = LowercaseWord UnderscoreSeparator LowercaseWord

LowercaseWord
    = [a-z] AdditionalCharacters*

AdditionalCharacters
    = Separator? Alphanumeric+

Separator
    = "-" / "~" / "_"

Alphanumeric
    = [a-zA-Z0-9]

UnderscoreSeparator
    = "__"
```

# Links

*  [Source code](http://github.com/csdms/standard_names): The
   *standard_names* source code repository.
*  [Documentation](http://standard-names.readthedocs.io/): User documentation
   for *standard_names*
*  [Get](http://standard-names.readthedocs.io/en/latest/getting.html):
   Installation instructions
*  [Registry](http://github.com/csdms/standard_names_registry): The
   official registry of CSDMS Standard Names.
