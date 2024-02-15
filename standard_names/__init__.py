"""The CSDMS Standard Names"""
from importlib.metadata import version

from .error import BadNameError
from .error import BadRegistryError
from .registry import NamesRegistry
from .standardname import StandardName
from .standardname import is_valid_name

__version__ = version("standard-names")
__all__ = [
    "StandardName",
    "is_valid_name",
    "NamesRegistry",
    "BadNameError",
    "BadRegistryError",
]
