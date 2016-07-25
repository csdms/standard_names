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


def main():
    """
    Build a list of CSDMS standard names for YAML description files.
    """
    import argparse

    parser = argparse.ArgumentParser(
        'Scan a model description file for CSDMS standard names')
    parser.add_argument('file', nargs='+', type=argparse.FileType('r'),
                        help='YAML file describing model exchange items')
    args = parser.parse_args()

    names = NamesRegistry(args.file)

    formatter = FORMATTERS['yaml']

    print('%YAML 1.2')
    print('---')

    print(os.linesep.join([
        formatter(names.names, sorted=True, heading='names'),
        '---',
        formatter(names.objects, sorted=True, heading='objects'),
        '---',
        formatter(names.quantities, sorted=True, heading='quantities'),
        '---',
        formatter(names.operators, sorted=True, heading='operators'),
        '...',
    ]))


if __name__ == '__main__':
    main()
