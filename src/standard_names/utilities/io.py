#! /usr/bin/env python
"""Some IO functions for standard_names package."""

import os
import re
import sys
from collections.abc import Callable
from collections.abc import Iterable
from typing import Any
from typing import TextIO

from standard_names.error import BadNameError
from standard_names.registry import NamesRegistry
from standard_names.utilities.decorators import format_as_plain_text
from standard_names.utilities.decorators import format_as_wiki
from standard_names.utilities.decorators import format_as_yaml
from standard_names.utilities.decorators import google_doc
from standard_names.utilities.decorators import plain_text
from standard_names.utilities.decorators import url


def _list_to_string(lines: Iterable[str], **kwds: dict[str, Any]) -> str:
    """Join strings with the line separator.

    Concatonate a list of strings into one big string using the line separator
    as a joiner.

    Parameters
    ----------
    lines : iterable of str
        String to join.
    sorted : bool, optional
        Sort the strings before joining them.
    newline : str, optional
        Newline character to use for output.

    Returns
    -------
    str
        The joined strings.

    Examples
    --------
    >>> from __future__ import print_function
    >>> import standard_names as csn
    >>> print(csn.utilities.io._list_to_string(('foo', 'bar'), newline='\\n'))
    foo
    bar
    >>> print(csn.utilities.io._list_to_string(('foo', 'bar'), sorted=True, newline='\\n'))
    bar
    foo
    """
    newline = kwds.pop("newline", os.linesep)
    if not isinstance(newline, str):
        raise ValueError("newline keyword must be of type str")
    if kwds.pop("sorted", False):
        sorted_lines = list(lines)
        sorted_lines.sort()
        return newline.join(sorted_lines)
    else:
        return newline.join(lines)


def _scrape_stream(stream: TextIO, regex: str = r"\b\w+__\w+") -> NamesRegistry:
    """Scrape standard names from stream matching a regular expression.

    Parameters
    ----------
    stream : file_like
        File-like object from which to read (only a ``read`` method is
        necessary).
    regex : str, optional
        A regular expression that indicates a word to scrape.

    Returns
    -------
    NamesRegistry
        The scraped words.

    Examples
    --------
    >>> from standard_names.utilities.io import _scrape_stream
    >>> from io import StringIO

    >>> stream = StringIO('''
    ... Some text with a standard name (air__temperature) in it.
    ... More words with more names: water__temperature. If a word matches
    ... the pattern but is not a valid name, ignore it (Air__Temperature
    ... is an example).
    ... ''')
    >>> names = _scrape_stream(stream)
    >>> sorted(names.names)
    ['air__temperature', 'water__temperature']
    """
    names = NamesRegistry()

    text = stream.read()
    words = re.findall(regex, text)
    for word in words:
        try:
            names.add(word)
        except BadNameError as error:
            print(
                "{name}: matches pattern but not a valid name. "
                "Ignoring.".format(name=error.name),
                file=sys.stderr,
            )

    return names


FORMATTERS: dict[str, Callable[..., str]] = {
    "plain": _list_to_string,
    "wiki": format_as_wiki(_list_to_string),
    "yaml": format_as_yaml(_list_to_string),
    "txt": format_as_plain_text(_list_to_string),
}


SCRAPERS: dict[str, Callable[..., NamesRegistry]] = {}
for decorator in [google_doc, url, plain_text]:
    SCRAPERS[decorator.__name__] = decorator(_scrape_stream)


_VALID_INTENTS = ["input", "output"]


def _find_unique_names(models: Iterable[dict[str, Any]]) -> NamesRegistry:
    """Find unique names in a iterable of StandardNames.

    Parameters
    ----------
    models : dict
        Dictionary of model information

    Returns
    -------
    NamesRegistry
        A collection of unique names.
    """
    names = NamesRegistry()
    for model in models:
        if isinstance(model["exchange items"], dict):
            new_names = []
            for intent in model["exchange items"]:
                if intent not in _VALID_INTENTS:
                    raise ValueError(f"{intent}: Bad intent")
                new_names.extend(model["exchange items"][intent])
        else:
            new_names = model["exchange items"]

        for new_name in new_names:
            names.add(new_name)

    return names


def from_model_file(stream: TextIO) -> NamesRegistry:
    """Read names from a model file.

    Get standard names from a YAML file listing standard names for particular
    models and produce the corresponding NamesRegistry.

    Parameters
    ----------
    stream : file_like
        YAML stream.

    Returns
    -------
    NamesRegistry
        A collection of names for the model file.
    """
    import yaml

    models = yaml.safe_load_all(stream)
    names = _find_unique_names(models)
    return names


def from_list_file(stream: TextIO) -> NamesRegistry:
    """Read names from a text file.

    Parameters
    ----------
    stream : file_like
        Source from which to read names (requires only a ``readline`` method).

    Returns
    -------
    NamesRegistry
        A collection of names read from the source.

    Examples
    --------
    >>> from standard_names.utilities.io import from_list_file
    >>> from io import StringIO

    >>> stream = StringIO('''
    ... air__temperature
    ... # A comment
    ... water__temperature # Another comment
    ... ''')
    >>> names = from_list_file(stream)
    >>> sorted(names.names)
    ['air__temperature', 'water__temperature']
    """
    names = NamesRegistry()
    for line in stream:
        if "#" in line:
            line = line[: line.find("#")]
        line = line.strip()
        if line:
            names.add(line)
    return names


def scrape(source: str, **kwargs: Any) -> NamesRegistry:
    """Scrape standard names for a named source.

    Parameters
    ----------
    source : str
        Name of the source.
    format: str, optional
        The format of the source. Valid values are given by the keys
        of the ``SCRAPERS` global. Currently this is ``google_doc``,
        ``url``, and ``plain_text`` (default is ``url``).

    Returns
    -------
    NamesRegistry
        A collection of names read from the source.
    """
    source_format = kwargs.pop("format", "url")
    if not isinstance(source_format, str):
        raise ValueError("source_format keyword must be of type str")

    return SCRAPERS[source_format](source, **kwargs)
