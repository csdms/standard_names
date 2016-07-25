#! /usr/bin/env python
"""
Example usage:
    snbuild data/models.yaml data/scraped.yaml \
            > standard_names/data/standard_names.yaml
"""
from __future__ import print_function

import os
from ..utilities.io import FORMATTERS
from ..registry import NamesRegistry


def snbuild(file):
    """Build a YAML-formatted database of names.

    Parameters
    ----------
    file : str
        Text file of names.

    Returns
    -------
    str
        YAML-formatted text of the names database.
    """
    names = NamesRegistry(file)

    formatter = FORMATTERS['yaml']

    lines = [
        '%YAML 1.2',
        '---',
        formatter(names.names, sorted=True, heading='names'),
        '---',
        formatter(names.objects, sorted=True, heading='objects'),
        '---',
        formatter(names.quantities, sorted=True, heading='quantities'),
        '---',
        formatter(names.operators, sorted=True, heading='operators'),
        '...',
    ]
    return os.linesep.join(lines)


def main():
    """
    Build a list of CSDMS standard names for YAML description files.

    Examples
    --------
    >>> import standard_names as csn
    >>> import sys
    >>> sys.argv = ['snbuild', '-h']
    >>> csn.cmd.snbuild.main()
    """
    import argparse

    parser = argparse.ArgumentParser(
        'Scan a model description file for CSDMS standard names')
    parser.add_argument('file', nargs='+', type=argparse.FileType('r'),
                        help='YAML file describing model exchange items')
    args = parser.parse_args()

    print(snbuild(args.file))


if __name__ == '__main__':
    main()
