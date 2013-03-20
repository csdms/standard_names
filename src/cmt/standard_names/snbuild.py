#! /usr/bin/env python
"""
Example usage:
    snbuild data/models.yaml data/scraped.yaml \
            > standard_names/data/standard_names.yaml
"""

import os
from cmt.standard_names import (from_model_file, FORMATTERS, Collection)


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
        names |= from_model_file(model_file)

    formatter = FORMATTERS['yaml']

    print '%YAML 1.2'
    print '---'

    print os.linesep.join([
        formatter(names.unique_names(), sorted=True, heading='names'),
        '---',
        formatter(names.unique_objects(), sorted=True, heading='objects'),
        '---',
        formatter(names.unique_quantities(), sorted=True,
                  heading='quantities'),
        '---',
        formatter(names.unique_operators(), sorted=True, heading='operators'),
        '...',
    ])

if __name__ == '__main__':
    main()
