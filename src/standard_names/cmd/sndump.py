#! /usr/bin/env python
"""
Example usage:
    sndump -n -o -q -op --format=wiki > standard_names.wiki
"""

import argparse
import os
from collections.abc import Iterable
from collections.abc import Sequence
from typing import Any

from standard_names.registry import NamesRegistry
from standard_names.utilities.io import FORMATTERS

_FORMATS = FORMATTERS.keys()


def sndump(
    file: str | None = None,
    format: str = "plain",
    sorted: bool = True,
    keys: str | Iterable[str] | None = None,
    newline: str | None = None,
) -> str:
    """Dump a registry to different formats.

    Parameters
    ----------
    file : str, optional
        Name of a registry file of names.
    format : {'plain'}, optional
        Output format.
    sorted : bool, optional
        Sort results.
    keys : {'names, 'objects', 'quantities', 'operators'} or iterable
        Standard Name element or elements to print.
    newline : str, optional
        Specify the newline character to use for output.

    Examples
    --------
    >>> import os
    >>> from io import StringIO
    >>> from standard_names.cmd.sndump import sndump

    >>> lines = os.linesep.join(['air__temperature', 'water__temperature'])
    >>> names = StringIO(lines)

    >>> print(sndump(names, newline='\\n'))
    ...     # doctest: +REPORT_NDIFF
    air__temperature
    water__temperature
    """
    newline = newline or os.linesep
    if isinstance(keys, str):
        keys = (keys,)
    keys = keys or ("names",)

    if file is None:
        names = NamesRegistry.from_latest()
    elif isinstance(file, str) and os.path.isfile(file):
        names = NamesRegistry.from_path(file)
    else:
        names = NamesRegistry(file)

    lines = []
    formatter = FORMATTERS[format]
    for key in keys:
        list_to_print = getattr(names, key)
        lines.append(
            formatter(
                list_to_print, sorted=sorted, heading=key, level=2, newline=newline
            )
        )

    return newline.join(lines)


class CustomAction(argparse.Action):
    """Keep track of the order of options are given on the command line."""

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None:
        if "ordered_args" not in namespace:
            namespace.ordered_args = []
        previous = namespace.ordered_args
        previous.append(self.dest)
        namespace.ordered_args = previous


def main(argv: tuple[str] | None = None) -> str:
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
    parser = argparse.ArgumentParser("Dump known standard names")

    parser.add_argument(
        "-n", nargs=0, dest="names", help="Print standard names", action=CustomAction
    )
    parser.add_argument(
        "-o",
        nargs=0,
        dest="objects",
        help="Print standard objects",
        action=CustomAction,
    )
    parser.add_argument(
        "-q",
        nargs=0,
        dest="quantities",
        help="Print standard quantities",
        action=CustomAction,
    )
    parser.add_argument(
        "-op",
        nargs=0,
        dest="operators",
        help="Print standard operators",
        action=CustomAction,
    )

    parser.add_argument(
        "file", type=argparse.FileType("r"), default=None, help="Read names from a file"
    )
    parser.add_argument(
        "--unsorted", action="store_true", default=False, help="Do not sort names"
    )
    parser.add_argument(
        "--format", choices=_FORMATS, default="plain", help="Output format"
    )

    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)

    try:
        keys = args.ordered_args
    except AttributeError:
        keys = ["names"]

    return sndump(
        file=args.file, format=args.format, sorted=not args.unsorted, keys=keys
    )


def run() -> None:
    print(main())
