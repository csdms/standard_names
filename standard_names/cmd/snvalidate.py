#! /usr/bin/env python
"""Validate a list of names."""
from __future__ import print_function

import os
import sys
import argparse

from ..registry import NamesRegistry
from ..standardname import BadRegistryError


def main():
    """Validate a list of names."""
    parser = argparse.ArgumentParser("Validate a list of standard names")

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+',
                        default=None,
                        help='Read names from a file')

    args = parser.parse_args()

    try:
        names = NamesRegistry(args.file)
    except BadRegistryError as err:
        # print('List contains invalid names', file=sys.stderr)
        print(os.linesep.join(err.names), file=sys.stderr)
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
