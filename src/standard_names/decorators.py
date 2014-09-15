#! /usr/bin/env python
"""
Some decorators for the CmtStandardNames package.
"""

import os


def format_as_wiki(func):
    """
    Decoratate a function that reads lines from a file. Put some wiki
    formatting around each line of the file and add a header, and
    footer.
    """
    def _wrapped(lines, **kwds):
        """
        Decorate a list of strings.

        :lines: List of strings
        :returns: Decorated strings concatoranted with line separators
        """
        heading = kwds.pop('heading', None)
        heading_level = kwds.pop('level', 1)
        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        wiki_lines = []
        for line in lines:
            wiki_lines.append(line + '<br/>')
        wiki_lines.insert(0, '<tt>')
        wiki_lines.append('</tt>')

        if heading:
            pre = '=' * heading_level
            wiki_lines.insert(0, '%s %s %s' % (pre, heading.title(), pre))

        return os.linesep.join(wiki_lines)
    return _wrapped


def format_as_yaml(func):
    """
    Decoratate a function that reads lines from a file. Put some YAML
    formatting around each line of the file and add a header, and
    footer.
    """
    def _wrapped(lines, **kwds):
        """
        Decorate a list of strings.

        :lines: List of strings
        :returns: Decorated strings concatoranted with line separators
        """
        heading = kwds.pop('heading', None)
        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        if heading:
            yaml_lines = ['%s:' % heading]
            indent = 2
        else:
            yaml_lines = []
            indent = 0

        for line in lines:
            yaml_lines.append('%s- %s' % (' ' * indent, line))

        return os.linesep.join(yaml_lines)
    return _wrapped


def format_as_plain_text(func):
    def _wrapped(lines, **kwds):
        heading = kwds.pop('heading', None)
        text = func(lines, **kwds)
        lines = text.split(os.linesep)

        if heading:
            stripped_lines = ['# %s' % heading]
        else:
            stripped_lines = []

        for line in lines:
            stripped_lines.append(line.strip())

        return os.linesep.join(stripped_lines)
    return _wrapped


def plain_text(func):
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a given name.
    """
    def _wrapped(name, **kwds):
        """
        Open a file by name.

        :name: Name of the file as a string.
        """
        with open(name, 'r') as file_like:
            rtn = func(file_like, **kwds)
        return rtn
    return _wrapped


def url(func):
    """
    Decoratate a function that reads from a file-like object. The decorated
    function will instead read from a file with a URL.
    """
    def _wrapped(name, **kwds):
        """
        Open a URL by name.

        :name: Name of the URL as a string.
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
        """
        Open a Google Doc file by name.

        :name: Name of the Google Doc file as a string.
        """
        import subprocess
        import tempfile

        (_, tfile) = tempfile.mkstemp(text=True)

        try:
            subprocess.check_call(['google', 'docs', 'get', name, tfile])
        except subprocess.CalledProcessError:
            raise
        else:
            with open(tfile, 'r') as file_like:
                rtn = func(file_like, **kwds)
        finally:
            os.remove(tfile)

        return rtn
    return _wrapped
