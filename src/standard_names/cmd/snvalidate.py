#! /usr/bin/env python
"""Validate a list of names."""

import argparse
import os
import sys

from standard_names.error import BadRegistryError
from standard_names.registry import NamesRegistry


def main(argv: tuple[str] | None = None) -> int:
    """Validate a list of names.

    Examples
    --------
    >>> import os
    >>> from standard_names.registry import _get_latest_names_file
    >>> from standard_names.cmd.snvalidate import main

    >>> (fname, _) = _get_latest_names_file()
    >>> main([fname])
    0

    >>> import tempfile
    >>> (fd, fname) = tempfile.mkstemp()
    >>> os.close(fd)

    >>> with open(fname, 'w') as fp:
    ...     print('air__temperature', file=fp)
    ...     print('Water__temperature', file=fp)
    ...     print('water_temperature', file=fp)

    >>> main([fp.name])
    2

    >>> os.remove(fname)
    """
    parser = argparse.ArgumentParser("Validate a list of standard names")

    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        nargs="*",
        help="Read names from a file",
    )

    args = parser.parse_args(argv)

    error_count = 0
    for file in args.file:
        try:
            NamesRegistry(file)
        except BadRegistryError as err:
            print(os.linesep.join(err.names), file=sys.stderr)
            error_count += len(err.names)
    return error_count


if __name__ == "__main__":
    SystemExit(main())
