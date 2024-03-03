![[Python][pypi-link]][python-badge]
![[Build Status][build-link]][build-badge]
![[PyPI][pypi-link]][pypi-badge]
![[Build Status][anaconda-link]][anaconda-badge]


[anaconda-badge]: https://anaconda.org/conda-forge/standard_names/badges/version.svg
[anaconda-link]: https://anaconda.org/conda-forge/standard_names
[build-badge]: https://github.com/csdms/standard_names/actions/workflows/test.yml/badge.svg
[build-link]: https://github.com/csdms/standard_names/actions/workflows/test.yml
[csdms-workbench]: https://csdms.colorado.edu/wiki/Workbench
[pypi-badge]: https://badge.fury.io/py/standard_names.svg
[pypi-link]: https://pypi.org/project/standard_names/
[python-badge]: https://img.shields.io/pypi/pyversions/standard_names.svg

# standard_names

Python utilities for working with CSDMS Standard Names.

CSDMS Standard Names is an element of the [CSDMS Workbench][csdms-workbench],
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
