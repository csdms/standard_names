"""
The CSDMS Standard Names
"""

from .standardname import StandardName, BadNameError, is_valid_name
from .validnames import NAMES, OBJECTS, QUANTITIES, OPERATORS
from .decorators import format_as_wiki, format_as_yaml
from .decorators import google_doc, url, plain_text
from .collection import Collection
from .io import from_model_file, scrape, FORMATTERS, SCRAPERS
