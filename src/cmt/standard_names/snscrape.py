#! /usr/bin/env python
"""
Example usage:
    snscrape http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
             http://csdms.colorado.edu/wiki/CSN_Object_Templates \
             http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
            > data/scraped.yaml
"""

import os

from cmt.standard_names import FORMATTERS, SCRAPERS, scrape


_AS_YAML = FORMATTERS['yaml']

_DEFAULT_SEARCH = r'\b\w+__\w+'


def main():
    """
    Scrape standard names from a file or URL.
    """
    import argparse

    parser = argparse.ArgumentParser(
        "Scrape standard names from a file or URL")
    parser.add_argument('file', nargs='+', metavar='FILE',
                        help="URL or file to scrape")
    parser.add_argument('--reader', choices=SCRAPERS.keys(),
                        default='url',
                        help="Name of reader ")
    parser.add_argument('--regex', default=_DEFAULT_SEARCH,
                        help='Regular expression describing '
                             'a standard name (%s)' % _DEFAULT_SEARCH)

    args = parser.parse_args()

    kwds = dict(format=args.reader)
    if args.regex:
        kwds['regex'] = args.regex

    docs = {}
    for file_name in args.file:
        docs[file_name] = scrape(file_name, **kwds)

    documents = []
    for (name, name_list) in docs.items():
        documents.append(os.linesep.join([
            'model name: %s' % name,
            _AS_YAML(name_list, sorted=True, heading='exchange items')
        ]))

    docsep = os.linesep + '---' + os.linesep

    print '%YAML 1.2'
    print '---'
    print docsep.join(documents)
    print '...'


if __name__ == '__main__':
    main()
