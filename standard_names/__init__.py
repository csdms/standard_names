"""The CSDMS Standard Names"""
import pkg_resources
from .error import BadNameError, BadRegistryError
from .registry import NamesRegistry
from .standardname import StandardName, is_valid_name

__version__ = pkg_resources.get_distribution("standard-names").version
__all__ = [
    "StandardName",
    "is_valid_name",
    "NamesRegistry",
    "BadNameError",
    "BadRegistryError",
]
