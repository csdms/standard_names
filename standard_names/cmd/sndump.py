#! /usr/bin/env python
"""
Example usage:
    sndump -n -o -q -op --format=wiki > standard_names.wiki
"""
from __future__ import print_function

import os
import sys
import argparse

from ..registry import NamesRegistry
from ..utilities import FORMATTERS


_FORMATS = FORMATTERS.keys()


def sndump(file=None, format="plain", sorted=True, keys=None, newline=None):
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
    >>> from __future__ import print_function
    >>> import os
    >>> from six.moves import StringIO
    >>> import standard_names as csn

    >>> lines = os.linesep.join(['air__temperature', 'water__temperature'])
    >>> names = StringIO(lines)

    >>> print(csn.cmd.sndump.sndump(names, newline='\\n'))
    ...     # doctest: +REPORT_NDIFF
    air__temperature
    water__temperature
    """
    newline = newline or os.linesep
    keys = keys or ("names",)
    if file:
        args = (file,)
    else:
        args = ()

    names = NamesRegistry(*args)

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

    def __call__(self, parser, namespace, values, option_string=None):
        if not "ordered_args" in namespace:
            setattr(namespace, "ordered_args", [])
        previous = namespace.ordered_args
        previous.append(self.dest)
        setattr(namespace, "ordered_args", previous)


def main(args=None):
    """Dump a list of known standard names.

    Parameters
    ----------
    args : iterable of str, optional
        Arguments to pass to *parse_args*. If not provided, use ``sys.argv``.

    Examples
    --------
    >>> import os
    >>> import standard_names as csn
    >>> (fname, _) = csn.registry._get_latest_names_file()
    >>> registry = csn.NamesRegistry()

    >>> names = csn.cmd.sndump.main(['-n', fname]).split(os.linesep)
    >>> len(names) == len(registry)
    True

    >>> objects = csn.cmd.sndump.main(['-o', fname]).split(os.linesep)
    >>> len(objects) == len(registry.objects)
    True

    >>> names = csn.cmd.sndump.main(['-n', '-o', fname]).split(os.linesep)
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

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    try:
        keys = args.ordered_args
    except AttributeError:
        keys = ["names"]

    return sndump(
        file=args.file, format=args.format, sorted=not args.unsorted, keys=keys
    )


def run():
    print(main())
