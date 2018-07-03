#! /usr/bin/env python
"""
Example usage:
    snscrape http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
             http://csdms.colorado.edu/wiki/CSN_Object_Templates \
             http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
            > data/scraped.yaml
"""
from __future__ import print_function

import os

from ..utilities import FORMATTERS, SCRAPERS, scrape


_AS_TXT = FORMATTERS["txt"]

_DEFAULT_SEARCH = r"\b[\w~-]+__[\w~-]+"


def snscrape(files, with_headers=False, regex=None, format="url", newline=None):
    """Scrape names from a URL.

    Parameters
    ----------
    files : iterable of str
        List of files or URL to scrape.
    with_headers : bool, optional
        Include headers in the output that indicate the name of the source.
    regex : str, optional
        A regular expression that defines what a Standard Name is.
    format : {'url', 'plain_text'}, optional
        The format of the target that's being scraped.
    newline : str, optional
        Newline character to use for output.

    Returns
    -------
    str
        The scraped names.

    Examples
    --------
    >>> from __future__ import print_function
    >>> from six.moves import StringIO
    >>> import standard_names as csn

    >>> file1 = StringIO(\"\"\"
    ... A file is one name, which is air__temperature.
    ... \"\"\")
    >>> file2 = StringIO(\"\"\"
    ... A file is two names: air__temperature, and water__temperature.
    ... \"\"\")

    >>> lines = csn.cmd.snscrape.snscrape([file1, file2], format='plain_text')
    >>> sorted(lines.split(os.linesep))
    ['air__temperature', 'air__temperature', 'water__temperature']
    """
    newline = newline or os.linesep
    regex = regex or _DEFAULT_SEARCH

    docs = {}
    for file_name in files:
        docs[file_name] = scrape(file_name, regex=regex, format=format)

    documents = []
    for (name, name_list) in docs.items():
        if with_headers:
            heading = "Scraped from %s" % name
        else:
            heading = None
        documents.append(_AS_TXT(name_list, sorted=True, heading=heading))

    return newline.join(documents)


def main(args=None):
    """Scrape standard names from a file or URL.

    Examples
    --------
    >>> import os
    >>> import tempfile
    >>> import standard_names as csn

    >>> contents = \"\"\"
    ... A file with text and names (air__temperature) mixed in. Some names
    ... have double underscores (like, Water__Temperature) by are not
    ... valid names. Others, like water__temperature, are good.
    ... \"\"\"

    >>> (fd, fname) = tempfile.mkstemp()
    >>> os.close(fd)

    >>> with open(fname, 'w') as fp:
    ...     print(contents, file=fp)

    >>> names = csn.cmd.snscrape.main(
    ...     [fp.name, '--reader=plain_text', '--no-headers'])
    >>> names.split(os.linesep)
    ['air__temperature', 'water__temperature']

    >>> os.remove(fname)
    """
    import argparse

    parser = argparse.ArgumentParser("Scrape standard names from a file or URL")
    parser.add_argument("file", nargs="+", metavar="FILE", help="URL or file to scrape")
    parser.add_argument(
        "--reader", choices=SCRAPERS.keys(), default="url", help="Name of reader"
    )
    parser.add_argument(
        "--regex",
        default=_DEFAULT_SEARCH,
        help="Regular expression describing " "a standard name (%s)" % _DEFAULT_SEARCH,
    )
    parser.add_argument(
        "--no-headers", action="store_true", help="Do not print headers between scrapes"
    )

    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)

    return snscrape(
        args.file,
        with_headers=not args.no_headers,
        regex=args.regex,
        format=args.reader,
    )


def run():
    print(main())
