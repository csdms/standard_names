#! /usr/bin/env python
"""Some decorators for the CmtStandardNames package."""

import os

from six import string_types


def format_as_wiki(func):
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

    def _wrapped(lines, **kwds):
        """Decorate a list of strings.

        :lines: List of strings
        :returns: Decorated strings concatoranted with line separators
        """
        newline = kwds.pop("newline", os.linesep)
        heading = kwds.pop("heading", None)
        heading_level = kwds.pop("level", 1)

        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        wiki_lines = []
        for line in lines:
            wiki_lines.append(line + "<br/>")
        wiki_lines.insert(0, "<tt>")
        wiki_lines.append("</tt>")

        if heading:
            pre = "=" * heading_level
            wiki_lines.insert(0, "%s %s %s" % (pre, heading.title(), pre))

        return newline.join(wiki_lines)

    return _wrapped


def format_as_yaml(func):
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

    def _wrapped(lines, **kwds):
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

        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        if heading:
            yaml_lines = ["%s:" % heading]
            indent = 2
        else:
            yaml_lines = []
            indent = 0

        items = [line for line in lines if line]
        if items:
            for line in items:
                yaml_lines.append("%s- %s" % (" " * indent, line))
        else:
            yaml_lines.append("%s[]" % (" " * indent))

        return newline.join(yaml_lines)

    return _wrapped


def format_as_plain_text(func):
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

    def _wrapped(lines, **kwds):
        heading = kwds.pop("heading", None)
        newline = kwds.pop("newline", os.linesep)

        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        if heading:
            stripped_lines = ["# %s" % heading]
        else:
            stripped_lines = []

        for line in lines:
            stripped_lines.append(line.strip())

        return newline.join(stripped_lines)

    return _wrapped


def plain_text(func):
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a given name.
    """

    def _wrapped(name, **kwds):
        """Open a file by name.

        Parameters
        ----------
        name : str
            Name of the file as a string.
        """
        if isinstance(name, string_types):
            with open(name, "r") as file_like:
                rtn = func(file_like, **kwds)
        else:
            rtn = func(name, **kwds)
        return rtn

    return _wrapped


def url(func):
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a URL.
    """

    def _wrapped(name, **kwds):
        """Open a URL by name.

        Parameters
        ----------
        name : str
            Name of the URL as a string.
        """
        import urllib

        file_like = urllib.urlopen(name)
        rtn = func(file_like, **kwds)
        return rtn

    return _wrapped


def google_doc(func):
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a remote Google Doc file.
    """

    def _wrapped(name, **kwds):
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
            with open(tfile, "r") as file_like:
                rtn = func(file_like, **kwds)
        finally:
            os.remove(tfile)

        return rtn

    return _wrapped
