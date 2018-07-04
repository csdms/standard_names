#! /usr/bin/env python
"""Validate a list of names."""
from __future__ import print_function

import os
import sys
import argparse

from ..registry import NamesRegistry
from ..error import BadRegistryError


def main(args=None):
    """Validate a list of names.

    Examples
    --------
    >>> from __future__ import print_function
    >>> import os
    >>> import standard_names as csn

    >>> (fname, _) = csn.registry._get_latest_names_file()
    >>> csn.cmd.snvalidate.main([fname])
    0

    >>> import tempfile
    >>> (fd, fname) = tempfile.mkstemp()
    >>> os.close(fd)

    >>> with open(fname, 'w') as fp:
    ...     print('air__temperature', file=fp)
    ...     print('Water__temperature', file=fp)
    ...     print('water_temperature', file=fp)

    >>> csn.cmd.snvalidate.main([fp.name])
    2

    >>> os.remove(fname)
    """
    parser = argparse.ArgumentParser("Validate a list of standard names")

    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        nargs="+",
        default=None,
        help="Read names from a file",
    )

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    try:
        names = NamesRegistry(args.file)
    except BadRegistryError as err:
        print(os.linesep.join(err.names), file=sys.stderr)
        return len(err.names)
    else:
        return 0


def run():
    sys.exit(main())
