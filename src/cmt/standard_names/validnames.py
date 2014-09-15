#! /usr/bin/env python
"""
Collection of valid standard names.
"""

import os
import yaml
import types


NAMES = set()
OBJECTS = set()
QUANTITIES = set()
OPERATORS = set()


def load_names_from_yaml(file):
    """
    Load valid standard names from a data base of known valid names.
    """
    constituents = yaml.load_all(file)

    valid_clauses = {}
    for constituent in constituents:
        for (name, clauses) in constituent.items():
            assert(name in ['names', 'objects', 'quantities',
                            'operators'])
            try:
                valid_clauses[name] |= set(clauses)
            except KeyError:
                valid_clauses[name] = set(clauses)

    return {
        'names': valid_clauses.pop('names', set()),
        'objects': valid_clauses.pop('objects', set()),
        'quantities': valid_clauses.pop('quantities', set()),
        'operators': valid_clauses.pop('operators', set()),
    }


def _load_names():
    """
    Load valid standard names from a data base of known valid names.
    """
    names_file = os.path.join(os.path.dirname(__file__),
                              'data', 'standard_names.yaml')
    with open(names_file, 'r') as names_fp:
        names = load_names_from_yaml(names_fp)

    for name in names:
        globals()[name.upper()] = names[name]


_load_names()


if __name__ == '__main__':
    for standard_name in NAMES:
        print standard_name
