#! /usr/bin/env python

import os

from standard_names import (StandardName, Collection)
from standard_names import (wiki, yaml)
from standard_names import (google_doc, url, file)

def _list_to_string (lines, **kwds):
    sorted = kwds.pop ('sorted', False)

    if sorted:
        sorted_lines = list (lines)
        sorted_lines.sort ()
        return os.linesep.join (sorted_lines)
    else:
        return os.linesep.join (lines)

def _scrape_stream (stream, regex=r'\b\w+__\w+'):
    import re
    names = Collection ()

    text = stream.read ()
    words = re.findall (regex, text)
    for word in words:
        names.add (word)

    return names

FORMATTERS = dict (plain=_list_to_string)
for decorator in [wiki, yaml]:
    FORMATTERS[decorator.__name__] = decorator (_list_to_string)

SCRAPERS = dict ()
for decorator in [google_doc, url, file]:
    SCRAPERS[decorator.__name__] = decorator (_scrape_stream)

def _find_unique_names (models):
    """
    Find unique names in a iterable of StandardNames.
    """
    names = Collection ()
    for model in models:
        try:
            intent = model['exchange items'].keys ()
            new_names = []
            for key in model['exchange items']:
                try:
                    assert (key in ['input', 'output'])
                except AssertionError:
                    raise KeyError (key)
                new_names.extend (model['exchange items'][key])
        except AttributeError:
            new_names = model['exchange items']

        for name in new_names:
            names.add (StandardName (name))

    return names

def from_model_file (file):
    import yaml
    models = yaml.load_all (file)
    names = _find_unique_names (models)
    return names

def scrape (file_name, **kwds):
    format = kwds.pop ('format', 'url')

    return SCRAPERS[format] (file_name, **kwds)


