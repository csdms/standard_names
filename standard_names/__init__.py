"""The CSDMS Standard Names"""

from .standardname import StandardName, is_valid_name
from .registry import NamesRegistry
from .error import BadNameError, BadRegistryError


from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
