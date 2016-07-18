#! /usr/bin/env python
"""
Collection of valid standard names.
"""

import os
import yaml
import types
import warnings

from .standardname import StandardName, BadNameError


NAMES = set()
OBJECTS = set()
QUANTITIES = set()
OPERATORS = set()


def load_names_from_yaml(file):
    """
    Load valid standard names from a database of known valid names.
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


def load_names_from_txt(file, onerror='raise'):
    if onerror not in ('pass', 'raise', 'warn'):
        return ValueError('value for onerror keyword not understood')

    bad_names = set()
    names = set()
    with open(file, 'r') as fp:
        for name in fp:
            name = name.strip()
            if name:
                try:
                    csn = StandardName(name)
                except BadNameError:
                    bad_names.add(name)
                else:
                    names.add(csn)

    if bad_names:
        for name in bad_names:
            warnings.warn('{name}: not a valid name'.format(name=name))
        if onerror == 'raise':
            raise ValueError('poorly formed name(s)')

    return names


def _load_names():
    """
    Load valid standard names from a database of known valid names.
    """
    names_file = os.path.join(os.path.dirname(__file__),
                              'data', 'standard_names.yaml')
    # with open(names_file, 'r') as names_fp:
    #     names = load_names_from_yaml(names_fp)

    # for name in names:
    #     globals()[name.upper()] = names[name]

    names_file = os.path.join(os.path.dirname(__file__),
                              'data', 'names.txt')

    names = load_names_from_txt(names_file)
    for name in names:
        NAMES.add(name.name)
        OBJECTS.add(name.object)
        QUANTITIES.add(name.quantity)
        for op in name.operators:
            OPERATORS.add(op)


_load_names()


if __name__ == '__main__':
    for standard_name in NAMES:
        print standard_name
