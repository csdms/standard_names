#! /usr/bin/env python
"""
Example usage:
    snbuild data/models.yaml data/scraped.yaml \
            > standard_names/data/standard_names.yaml
"""

import os

from standard_names.registry import NamesRegistry
from standard_names.utilities.io import FORMATTERS


def snbuild(file: str, newline: str | None = None) -> str:
    """Build a YAML-formatted database of names.

    Parameters
    ----------
    file : str
        Text file of names.
    newline : str, optional
        Newline character to use for output.

    Returns
    -------
    str
        YAML-formatted text of the names database.

    Examples
    --------
    >>> import os
    >>> from io import StringIO
    >>> from standard_names.cmd.snbuild import snbuild

    >>> lines = os.linesep.join(['air__temperature', 'water__temperature'])
    >>> names = StringIO(lines)

    >>> print(snbuild(names, newline='\\n'))
    %YAML 1.2
    ---
    names:
      - air__temperature
      - water__temperature
    ---
    objects:
      - air
      - water
    ---
    quantities:
      - temperature
    ---
    operators:
      []
    ...
    """
    newline = newline or os.linesep
    if isinstance(file, str) and os.path.isfile(file):
        names = NamesRegistry.from_path(file)
    else:
        names = NamesRegistry(file)

    formatter = FORMATTERS["yaml"]

    lines = [
        "%YAML 1.2",
        "---",
        formatter(names.names, sorted=True, heading="names", newline=newline),
        "---",
        formatter(names.objects, sorted=True, heading="objects", newline=newline),
        "---",
        formatter(names.quantities, sorted=True, heading="quantities", newline=newline),
        "---",
        formatter(names.operators, sorted=True, heading="operators", newline=newline),
        "...",
    ]
    return newline.join(lines)


def main(argv: tuple[str] | None = None) -> str:
    """Build a list of CSDMS standard names for YAML description files."""
    import argparse

    parser = argparse.ArgumentParser(
        "Scan a model description file for CSDMS standard names"
    )
    parser.add_argument(
        "file",
        nargs="+",
        type=argparse.FileType("r"),
        help="YAML file describing model exchange items",
    )

    if argv is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(argv)

    return snbuild(args.file)


def run() -> None:
    print(main())
