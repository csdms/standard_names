"""The CSDMS Standard Names"""

from .standardname import StandardName, is_valid_name
from .registry import NamesRegistry
from .error import BadNameError, BadRegistryError


__version__ = "0.2.2"


def check():
    from nose.core import run

    run("standard_names")

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
