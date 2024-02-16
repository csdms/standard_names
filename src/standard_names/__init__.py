"""The CSDMS Standard Names"""
from standard_names._version import __version__
from standard_names.registry import NamesRegistry
from standard_names.standardname import StandardName
from standard_names.standardname import is_valid_name

__all__ = [
    "__version__",
    "StandardName",
    "is_valid_name",
    "NamesRegistry",
]
