#! /usr/bin/env python
"""Some IO functions for standard_names package."""
from __future__ import print_function

import os
import sys

from . import StandardName, BadNameError
from .decorators import (format_as_wiki, format_as_yaml, format_as_plain_text)
from . import (google_doc, url, plain_text)
from .registry import NamesRegistry


class Error(Exception):

    """Base exception for this module."""

    pass


class BadIntentError(Error):

    """Error to indicate a bad key for intent."""

    def __init__(self, key, valid_keys):
        super(BadIntentError, self).__init__()
        self._key = key
        self._valid_keys = valid_keys

    def __str__(self):
        return '%s: Should be one of %s' % (self._key,
                                            ','.join(self._valid_keys))


def _list_to_string(lines, **kwds):
    """Join strings with the line separator.

    Concatonate a list of strings into one big string using the line separator
    as a joiner.

    Parameters
    ----------
    lines : iterable of str
        String to join.
    sorted : bool, optional
        Sort the strings before joining them.

    Returns
    -------
    str
        The joined strings.
    """
    sort_list = kwds.pop('sorted', False)

    if sort_list:
        sorted_lines = list(lines)
        sorted_lines.sort()
        return os.linesep.join(sorted_lines)
    else:
        return os.linesep.join(lines)


def _scrape_stream(stream, regex=r'\b\w+__\w+'):
    """Scrape standard names from stream matching a regular expression.

    Parameters
    ----------
    stream : file_like
        File-like object from which to read (only a ``read`` method is
        necessary).
    regex : str, optional
        A regular expression that indicates a word to scrape.

    Returns
    -------
    NamesRegistry
        The scraped words.
    """
    import re
    names = NamesRegistry(None)

    text = stream.read()
    words = re.findall(regex, text)
    for word in words:
        try:
            names.add(word)
        except BadNameError as error:
            print(error, file=sys.stderr)

    return names


FORMATTERS = {
    'plain': _list_to_string,
    'wiki': format_as_wiki(_list_to_string),
    'yaml': format_as_yaml(_list_to_string),
    'txt': format_as_plain_text(_list_to_string),
}
#for (name, decorator) in [('wiki', format_as_wiki), ('yaml', format_as_yaml),
#    ('txt', format_as_plain_text)]:
#    FORMATTERS[name] = decorator(_list_to_string)


SCRAPERS = dict()
for decorator in [google_doc, url, plain_text]:
    SCRAPERS[decorator.__name__] = decorator(_scrape_stream)


_VALID_INTENTS = ['input', 'output']


def _find_unique_names(models):
    """Find unique names in a iterable of StandardNames.

    Parameters
    ----------
    models : dict
        Dictionary of model information

    Returns
    -------
    NamesRegistry
        A collection of unique names.
    """
    names = NamesRegistry(None)
    for model in models:
        if isinstance(model['exchange items'], dict):
            new_names = []
            for intent in model['exchange items']:
                try:
                    assert(intent in _VALID_INTENTS)
                except AssertionError:
                    raise BadIntentError(intent, _VALID_INTENTS)
                new_names.extend(model['exchange items'][intent])
        else:
            new_names = model['exchange items']

        for new_name in new_names:
            names.add(new_name)
            # names.add(StandardName(new_name))

    return names


def from_model_file(stream):
    """Read names from a model file.

    Get standard names from a YAML file listing standard names for particular
    models and produce the corresponding NamesRegistry.

    Parameters
    ----------
    stream : file_like
        YAML stream.

    Returns
    -------
    NamesRegistry
        A collection of names for the model file.
    """
    import yaml
    models = yaml.load_all(stream)
    names = _find_unique_names(models)
    return names


def from_list_file(stream):
    """Read names from a text file.

    Parameters
    ----------
    stream : file_like
        Source from which to read names (requires only a ``readline`` method).

    Returns
    -------
    NamesRegistry
        A collection of names read from the source.
    """
    names = NamesRegistry(None)
    for line in stream:
        if not line.startswith('#'):
            names.add(line.strip())
    return names


def scrape(source, **kwds):
    """Scrape standard names for a named source.

    Parameters
    ----------
    source : str
        Name of the source.
    format: str, optional
        The format of the source. Valid values are given by the keys
        of the ``SCRAPERS` global. Currently this is ``google_doc``,
        ``url``, and ``plain_text`` (default is ``url``).

    Returns
    -------
    NamesRegistry
        A collection of names read from the source.
    """
    source_format = kwds.pop('format', 'url')

    return SCRAPERS[source_format](source, **kwds)
