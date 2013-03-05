#! /usr/bin/env python

import os

def wiki (f):
    def _wrapped (lines, **kwds):
        heading = kwds.pop ('heading', None)
        heading_level = kwds.pop ('level', 1)
        text = f(lines, **kwds)
        lines = text.split (os.linesep)

        wiki_lines = []
        for line in lines:
            wiki_lines.append (line + '<br/>')
        wiki_lines.insert (0, '<tt>')
        wiki_lines.append ('</tt>')

        if heading:
            pre = '=' * heading_level
            wiki_lines.insert (0, '%s %s %s' % (pre, heading.title (), pre))

        return os.linesep.join (wiki_lines)
    return _wrapped

def yaml (f):
    def _wrapped (lines, **kwds):
        heading = kwds.pop ('heading', None)
        text = f(lines, **kwds)
        lines = text.split (os.linesep)

        if heading:
            yaml_lines = ['%s:' % heading]
            indent = 2
        else:
            yaml_lines = []
            indent = 0

        for line in lines:
            yaml_lines.append ('%s- %s' % (' ' * indent, line))

        return os.linesep.join (yaml_lines)
    return _wrapped

def file (func):
    def _wrapped (file, **kwds):
        with open (file, 'r') as f:
            rtn = func (f, **kwds)
        return rtn
    return _wrapped

def url (func):
    def _wrapped (url, **kwds):
        import urllib

        f = urllib.urlopen (url)
        rtn = func (f, **kwds)
        return rtn
    return _wrapped

def google_doc (func):
    def _wrapped (file, **kwds):
        import subprocess
        import tempfile

        (f, tfile) = tempfile.mkstemp (text=True)

        try:
            subprocess.check_call (['google', 'docs', 'get', file, tfile])
        except subprocess.CalledProcessError as e:
            raise
        else:
            with open (tfile, 'r') as f:
                rtn = func (f, **kwds)
        finally:
            os.remove (tfile)

        return rtn
    return _wrapped

