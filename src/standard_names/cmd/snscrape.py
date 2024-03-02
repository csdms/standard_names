#! /usr/bin/env python
"""
Example usage:

```bash
snscrape http://csdms.colorado.edu/wiki/CSN_Quantity_Templates \
    http://csdms.colorado.edu/wiki/CSN_Object_Templates \
    http://csdms.colorado.edu/wiki/CSN_Operation_Templates \
    > data/scraped.yaml
```
"""

from collections.abc import Iterable

from standard_names.registry import NamesRegistry


def main(argv: tuple[str] | None = None) -> int:
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
    parser.add_argument("file", nargs="*", metavar="FILE", help="URL or file to scrape")

    args = parser.parse_args(argv)

    registry = NamesRegistry([])
    for file in args.file:
        registry |= NamesRegistry(search_file_for_names(file))
    print(registry.dumps(format_="text", fields=("names",)))

    return 0


def find_all_names(lines: Iterable[str], engine: str = "peg") -> set[str]:
    if engine == "regex":
        from standard_names.regex import findall
    elif engine == "peg":
        from standard_names.peg import findall
    else:
        raise ValueError(
            "engine not understood: {engine!r} is not one of 'regex', 'peg'"
        )

    names = set()
    for line in lines:
        names |= set(findall(line.strip()))

    return names


def search_file_for_names(path: str) -> set[str]:
    from urllib.request import urlopen

    names = set()
    if path.startswith(("http://", "https://")):
        with urlopen(path) as response:
            names = find_all_names(line.decode("utf-8") for line in response)
    else:
        with open(path) as fp:
            names = find_all_names(fp)

    return names


if __name__ == "__main__":
    SystemExit(main())
