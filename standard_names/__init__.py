"""The CSDMS Standard Names"""

from .standardname import StandardName, is_valid_name
from .registry import NamesRegistry
from .error import BadNameError, BadRegistryError

# from .decorators import (format_as_wiki, format_as_yaml, google_doc, url,
#                          plain_text)
# from .io import from_model_file, scrape, FORMATTERS, SCRAPERS

__version__ = '0.2.2'


def check():
    from nose.core import run
    run('standard_names')
