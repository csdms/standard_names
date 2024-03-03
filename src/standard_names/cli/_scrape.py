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
from __future__ import annotations

from collections.abc import Iterable
from urllib.request import urlopen

from standard_names.registry import NamesRegistry


def scrape_names(files: Iterable[str]) -> NamesRegistry:
    """Scrape standard names from a file or URL.

    Parameters
    ----------
    files : iterable of str
        Files to search for names.

    Returns
    -------
    NamesRegistry
        A registry of the names found in the files.
    """
    registry = NamesRegistry([])
    for file in files:
        registry |= NamesRegistry(search_file_for_names(file))
    return registry


def find_all_names(lines: Iterable[str], engine: str = "regex") -> set[str]:
    """Find standard names.

    Examples
    --------
    >>> from standard_names.cli._scrape import find_all_names

    >>> contents = '''
    ... A file with text and names (air__temperature) mixed in. Some names
    ... have double underscores (like, Water__Temperature) by are not
    ... valid names. Others, like water__temperature, or "wind__speed" are good.
    ... '''
    >>> sorted(find_all_names(contents.splitlines(), engine="regex"))
    ['air__temperature', 'water__temperature', 'wind__speed']

    >>> sorted(find_all_names(contents.splitlines(), engine="peg"))
    ['air__temperature', 'water__temperature', 'wind__speed']
    """
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
    names = set()
    if path.startswith(("http://", "https://")):
        with urlopen(path) as response:
            names = find_all_names(line.decode("utf-8") for line in response)
    else:
        with open(path) as fp:
            names = find_all_names(fp)

    return names
