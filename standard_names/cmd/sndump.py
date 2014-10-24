#! /usr/bin/env python
"""
Example usage:
    sndump -n -o -q -op --format=wiki > standard_names.wiki
"""
import sys
import argparse

from .. import (NAMES, OBJECTS, QUANTITIES, OPERATORS)
from .. import FORMATTERS
from ..validnames import load_names_from_yaml


_NAMES = dict(names=NAMES, objects=OBJECTS, quantities=QUANTITIES,
              operators=OPERATORS, )
_FORMATS = FORMATTERS.keys()


class CustomAction(argparse.Action):
    """
    Keep track of the order of options are given on the command line.
    """
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'ordered_args' in namespace:
            setattr(namespace, 'ordered_args', [])
        previous = namespace.ordered_args
        previous.append(self.dest)
        setattr(namespace, 'ordered_args', previous)


def main():
    """
    Dump a list of known standard names.
    """
    parser = argparse.ArgumentParser("Dump known standard names")

    parser.add_argument('-n', nargs=0, dest='names',
                        help='Print standard names', action=CustomAction)
    parser.add_argument('-o', nargs=0, dest='objects',
                        help='Print standard objects', action=CustomAction)
    parser.add_argument('-q', nargs=0, dest='quantities',
                        help='Print standard quantities',
                        action=CustomAction)
    parser.add_argument('-op', nargs=0, dest='operators',
                        help='Print standard operators', action=CustomAction)

    parser.add_argument('file', type=argparse.FileType('r'), default=None,
                        help='Read names from a file')
    parser.add_argument('--unsorted', action='store_true',
                        default=False, help='Do not sort names')
    parser.add_argument('--format', choices=_FORMATS,
                        default='plain', help='Output format')

    args = parser.parse_args()

    try:
        keys = args.ordered_args
    except AttributeError:
        keys = ['names']

    if args.file:
        names = load_names_from_yaml(args.file)
    else:
        names = _NAMES

    formatter = FORMATTERS[args.format]
    for key in keys:
        print formatter(names[key], sorted=not args.unsorted,
                        heading=key, level=2)


if __name__ == '__main__':
    main()
