#! /usr/bin/env python
"""Some decorators for the CmtStandardNames package."""

import os
from collections.abc import Callable
from collections.abc import Iterator
from typing import Any

from standard_names.registry import NamesRegistry


def format_as_wiki(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decoratate a function that reads lines from a file. Put some wiki
    formatting around each line of the file and add a header, and
    footer.

    Examples
    --------
    >>> from __future__ import print_function
    >>> import os
    >>> from standard_names.utilities.decorators import format_as_wiki

    >>> def func(lines):
    ...     return lines

    >>> wikize = format_as_wiki(func)
    >>> lines = os.linesep.join(['line 1', 'line 2'])
    >>> print(wikize(lines, heading='Lines', newline='\\n'))
    = Lines =
    <tt>
    line 1<br/>
    line 2<br/>
    </tt>
    """

    def _wrapped(file_like: Iterator[str], **kwds: Any) -> str:
        """Decorate a list of strings.

        :lines: List of strings
        :returns: Decorated strings concatoranted with line separators
        """
        newline = kwds.pop("newline", os.linesep)
        heading = kwds.pop("heading", None)
        heading_level = kwds.pop("level", 1)

        if not isinstance(newline, str):
            raise ValueError("newline keyword must be of type str")
        if not isinstance(heading, str) and heading is not None:
            raise ValueError("heading keyword must be of type str or None")
        if not isinstance(heading_level, int):
            raise ValueError("level keyword must be of type int")

        text = func(file_like, **kwds)
        lines = text.split(os.linesep)

        wiki_lines = ["<tt>"] + [line + "<br/>" for line in lines] + ["</tt>"]

        if heading is not None:
            pre = "=" * heading_level
            wiki_lines.insert(0, f"{pre} {heading.title()} {pre}")

        return newline.join(wiki_lines)

    return _wrapped


def format_as_yaml(func: Callable[..., str]) -> Callable[..., str]:
    """
    Decoratate a function that reads lines from a file. Put some YAML
    formatting around each line of the file and add a header, and
    footer.

    Examples
    --------
    >>> from __future__ import print_function
    >>> import os
    >>> from standard_names.utilities.decorators import format_as_yaml

    >>> def func(lines):
    ...     return lines

    >>> yamlize = format_as_yaml(func)
    >>> lines = os.linesep.join(['line 1', 'line 2'])
    >>> print(yamlize(lines, heading='Lines', newline='\\n'))
    Lines:
      - line 1
      - line 2
    >>> print(yamlize(lines, newline='\\n'))
    - line 1
    - line 2
    """

    def _wrapped(file_like: Iterator[str], **kwds: Any) -> str:
        """Decorate a list of strings.

        Parameters
        ---------
        lines : iterable or str
            List of strings

        Returns
        -------
        str
            Decorated strings concatoranted with line separators
        """
        heading = kwds.pop("heading", None)
        newline = kwds.pop("newline", os.linesep)

        if not isinstance(newline, str):
            raise ValueError("newline keyword must be of type str")
        if not isinstance(heading, str) and heading is not None:
            raise ValueError("heading keyword must be of type str or None")

        text = func(file_like, **kwds)
        lines = text.split(os.linesep)

        if heading is not None:
            yaml_lines = ["%s:" % heading]
            indent = 2
        else:
            yaml_lines = []
            indent = 0

        items = [line for line in lines if line]
        if items:
            for line in items:
                yaml_lines.append("{}- {}".format(" " * indent, line))
        else:
            yaml_lines.append("%s[]" % (" " * indent))

        return newline.join(yaml_lines)

    return _wrapped


def format_as_plain_text(func: Callable[..., str]) -> Callable[..., str]:
    """

    Examples
    --------
    >>> from __future__ import print_function
    >>> from standard_names.utilities.decorators import format_as_plain_text

    >>> def func(lines):
    ...     return lines

    >>> textize = format_as_plain_text(func)
    >>> lines = os.linesep.join(['line 1', 'line 2'])
    >>> print(textize(lines, heading='Lines', newline='\\n'))
    # Lines
    line 1
    line 2
    """

    def _wrapped(file_like: Iterator[str], **kwds: Any) -> str:
        heading = kwds.pop("heading", None)
        newline = kwds.pop("newline", os.linesep)

        if not isinstance(newline, str):
            raise ValueError("newline keyword must be of type str")
        if not isinstance(heading, str) and heading is not None:
            raise ValueError("heading keyword must be of type str or None")

        text = func(file_like, **kwds)
        lines = text.split(os.linesep)

        if heading:
            stripped_lines = ["# %s" % heading]
        else:
            stripped_lines = []

        for line in lines:
            stripped_lines.append(line.strip())

        return newline.join(stripped_lines)

    return _wrapped


def plain_text(func: Callable[..., NamesRegistry]) -> Callable[..., NamesRegistry]:
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a given name.
    """

    def _wrapped(name: str, **kwds: Any) -> NamesRegistry:
        """Open a file by name.

        Parameters
        ----------
        name : str
            Name of the file as a string.
        """
        if isinstance(name, str):
            with open(name) as file_like:
                rtn = func(file_like, **kwds)
        else:
            rtn = func(name, **kwds)
        return rtn

    return _wrapped


def url(func: Callable[..., NamesRegistry]) -> Callable[..., NamesRegistry]:
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a URL.
    """

    def _wrapped(name: str, **kwds: Any) -> NamesRegistry:
        """Open a URL by name.

        Parameters
        ----------
        name : str
            Name of the URL as a string.
        """
        from urllib.request import urlopen

        file_like = urlopen(name)
        rtn = func(file_like, **kwds)
        return rtn

    return _wrapped


def google_doc(func: Callable[..., NamesRegistry]) -> Callable[..., NamesRegistry]:
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a remote Google Doc file.
    """

    def _wrapped(name: str, **kwds: Any) -> NamesRegistry:
        """Open a Google Doc file by name.

        Parameters
        ----------
        name : str
            Name of the Google Doc file as a string.
        """
        import subprocess
        import tempfile

        (_, tfile) = tempfile.mkstemp(text=True)

        try:
            subprocess.check_call(["google", "docs", "get", name, tfile])
        except subprocess.CalledProcessError:
            raise
        else:
            with open(tfile) as file_like:
                rtn = func(file_like, **kwds)
        finally:
            os.remove(tfile)

        return rtn

    return _wrapped
