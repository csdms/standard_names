#! /usr/bin/env python
"""Validate a list of names."""

import argparse
import os
from collections.abc import Iterator

from standard_names.error import BadRegistryError
from standard_names.registry import NamesRegistry


def main(argv: tuple[str] | None = None) -> int:
    """Validate a list of names."""
    parser = argparse.ArgumentParser("Validate a list of standard names")

    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        nargs="*",
        help="Read names from a file",
    )

    args = parser.parse_args(argv)

    invalid_names = set()
    for file in args.file:
        invalid_names |= validate_names(file)

    print(os.linesep.join(invalid_names))

    return len(invalid_names)


def validate_names(names: Iterator[str]) -> set[str]:
    """Find invalid names.

    Examples
    --------
    >>> import os
    >>> import tempfile
    >>> from standard_names.registry import _get_latest_names_file
    >>> from standard_names.cmd.snvalidate import validate_names

    >>> (fname, _) = _get_latest_names_file()
    >>> with open(fname) as fp:
    ...     invalid_names = validate_names(fp)
    >>> len(invalid_names)
    0

    >>> names = [
    ...     "air__temperature",
    ...     "Water__temperature",
    ...     "water_temperature",
    ... ]
    >>> invalid_names = validate_names(names)
    >>> sorted(invalid_names)
    ['Water__temperature', 'water_temperature']
    """
    try:
        NamesRegistry(names)
    except BadRegistryError as err:
        invalid_names = set(err.names)
    else:
        invalid_names = set()

    return invalid_names


if __name__ == "__main__":
    SystemExit(main())
