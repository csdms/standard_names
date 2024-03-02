#! /usr/bin/env python
"""
Example usage:
    sndump -fn -fo -fq -fop --format=wiki names.txt > standard_names.wiki
"""

import argparse

from standard_names._format import FORMATTERS
from standard_names.registry import NamesRegistry


def main(argv: tuple[str] | None = None) -> int:
    """Dump a list of known standard names.

    Parameters
    ----------
    args : iterable of str, optional
        Arguments to pass to *parse_args*. If not provided, use ``sys.argv``.

    Examples
    --------
    >>> import os
    >>> from standard_names.registry import NamesRegistry
    >>> from standard_names.registry import _get_latest_names_file
    >>> from standard_names.cmd.sndump import main

    >>> (fname, _) = _get_latest_names_file()
    >>> registry = NamesRegistry.from_path(fname)

    >>> names = main(['-n', fname]).split(os.linesep)
    >>> len(names) == len(registry)
    True

    >>> objects = main(['-o', fname]).split(os.linesep)
    >>> len(objects) == len(registry.objects)
    True

    >>> names = main(['-n', '-o', fname]).split(os.linesep)
    >>> len(names) == len(registry) + len(registry.objects)
    True
    """
    VALID_FIELDS = {
        "op": "operators",
        "q": "quantities",
        "o": "objects",
        "n": "names",
    }
    parser = argparse.ArgumentParser("Dump known standard names")

    parser.add_argument(
        "file", type=argparse.FileType("r"), nargs="*", help="Read names from a file"
    )
    parser.add_argument(
        "--field", "-f", action="append", help="Fields to print", choices=VALID_FIELDS
    )
    parser.add_argument(
        "--sort", action=argparse.BooleanOptionalAction, help="Sort/don't sort names"
    )
    parser.add_argument(
        "--format", choices=FORMATTERS, default="text", help="Output format"
    )

    args = parser.parse_args(argv)
    fields = [VALID_FIELDS[field] for field in args.field] or None

    registry = NamesRegistry([])
    for file in args.file:
        registry |= NamesRegistry(file)
    print(registry.dumps(format_=args.format, sort=args.sort, fields=fields))

    return 0


if __name__ == "__main__":
    SystemExit(main())
