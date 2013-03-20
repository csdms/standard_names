#! /usr/bin/env python
"""
Collection of valid standard names.
"""

import os
import yaml


NAMES = set()
OBJECTS = set()
QUANTITIES = set()
OPERATORS = set()


def _load_names():
    """
    Load valid standard names from a data base of known valid names.
    """
    names_file = os.path.join(os.path.dirname(__file__),
                              'data', 'standard_names.yaml')
    with open(names_file, 'r') as names_db:
        constituents = yaml.load_all(names_db)

        valid_clauses = {}
        for constituent in constituents:
            for (name, clauses) in constituent.items():
                assert(name in ['names', 'objects', 'quantities',
                                'operators'])
                try:
                    valid_clauses[name] |= set(clauses)
                except KeyError:
                    valid_clauses[name] = set(clauses)

    globals()['NAMES'] = valid_clauses.pop('names', set())
    globals()['OBJECTS'] = valid_clauses.pop('objects', set())
    globals()['QUANTITIES'] = valid_clauses.pop('quantities', set())
    globals()['OPERATORS'] = valid_clauses.pop('operators', set())


_load_names()


if __name__ == '__main__':
    for standard_name in NAMES:
        print standard_name
