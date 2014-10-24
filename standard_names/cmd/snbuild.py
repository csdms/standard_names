#! /usr/bin/env python
"""
Example usage:
    snbuild data/models.yaml data/scraped.yaml \
            > standard_names/data/standard_names.yaml
"""

import os
from .. import (from_model_file, FORMATTERS, Collection)
from ..io import from_list_file


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

    names = Collection()
    for model_file in args.file:
        names |= from_list_file(model_file)

    formatter = FORMATTERS['yaml']

    print '%YAML 1.2'
    print '---'

    print os.linesep.join([
        formatter(names.names(), sorted=True, heading='names'),
        '---',
        formatter(names.objects(), sorted=True, heading='objects'),
        '---',
        formatter(names.quantities(), sorted=True, heading='quantities'),
        '---',
        formatter(names.operators(), sorted=True, heading='operators'),
        '...',
    ])


if __name__ == '__main__':
    main()
