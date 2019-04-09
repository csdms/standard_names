"""The CSDMS Standard Names"""

from ._version import get_versions
from .error import BadNameError, BadRegistryError
from .registry import NamesRegistry
from .standardname import StandardName, is_valid_name

__all__ = [
    "StandardName",
    "is_valid_name",
    "NamesRegistry",
    "BadNameError",
    "BadRegistryError",
]

__version__ = get_versions()["version"]
del get_versions
