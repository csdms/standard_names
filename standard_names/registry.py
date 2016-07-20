#! /usr/bin/env python
import os
import warnings
from glob import glob

from six import string_types

from .standardname import StandardName, BadNameError, BadRegistryError


def load_names_from_txt(file_like, onerror='raise'):
    if onerror not in ('pass', 'raise', 'warn'):
        return ValueError('value for onerror keyword not understood')

    bad_names = set()
    names = set()
    for name in file_like:
        name = name.strip()
        if name:
            try:
                csn = StandardName(name)
            except BadNameError:
                bad_names.add(name)
            else:
                names.add(csn)

    if bad_names:
        if onerror == 'warn':
            for name in bad_names:
                warnings.warn('{name}: not a valid name'.format(name=name))
        elif onerror == 'raise':
            raise BadRegistryError(bad_names)

    return names


def _get_latest_names_file():
    from distutils.version import StrictVersion

    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    data_file_pattern = os.path.join(data_dir, 'names-*.txt')
    files = [os.path.basename(file_) for file_ in glob(data_file_pattern)]

    newest = None
    for file in files:
        try:
            version = StrictVersion(file[len('names-'): -len('.txt')])
        except ValueError:
            pass
        else:
            if newest is None or version > newest:
                newest = version

    if newest:
        version = str(newest)
        names_file = os.path.join(
            data_dir, 'names-{version}.txt'.format(version=version))
        return names_file, version
    else:
        return None, None


class NamesRegistry(object):
    def __init__(self, *args, **kwds):
        if len(args) == 0:
            paths, version = _get_latest_names_file()
        elif len(args) == 1:
            paths, version = args[0], None
        else:
            raise ValueError('0 or 1 arguments expected')

        if paths is None:
            paths = []

        if isinstance(paths, string_types) or hasattr(paths, 'readline'):
            paths = [paths]

        self._names = set()
        self._objects = set()
        self._quantities = set()
        self._operators = set()

        self._version = version or '0.0.0'

        for path in paths:
            if isinstance(path, string_types):
                with open(path, 'r') as fp:
                    self._load(fp)
            else:
                self._load(path)

    def _load(self, file_like, onerror='raise'):
        for name in load_names_from_txt(file_like, onerror=onerror):
            self.add(name)

    @property
    def version(self):
        return self._version

    @property
    def names(self):
        return tuple(self._names)

    @property
    def objects(self):
        return tuple(self._objects)

    @property
    def quantities(self):
        return tuple(self._quantities)

    @property
    def operators(self):
        return tuple(self._operators)

    @classmethod
    def from_path(cls, path):
        return cls(path)

    def add(self, name):
        if not isinstance(name, StandardName):
            name = StandardName(name)

        self._names.add(name.name)
        self._objects.add(name.object)
        self._quantities.add(name.quantity)
        for op in name.operators:
            self._operators.add(op)

    def __contains__(self, name):
        if isinstance(name, StandardName):
            name = name.name
        return name in self._names

    def __len__(self):
        return len(self._names)

    def __iter__(self):
        for name in self._names:
            yield name

    def search(self, name):
        from difflib import get_close_matches
        return get_close_matches(name, self._names)

    def match(self, pattern):
        import re, fnmatch
        p = re.compile(fnmatch.translate(pattern))
        names = []
        for name in self._names:
            if p.match(name):
                names.append(name)
        return names

    def names_with(self, parts):
        if isinstance(parts, string_types):
            parts = (parts, )

        remaining_names = self._names
        for part in parts:
            names = []
            for name in remaining_names:
                if part in name:
                    names.append(name)
            remaining_names = names
        return names


REGISTRY = NamesRegistry()

NAMES = REGISTRY.names
OBJECTS = REGISTRY.objects
QUANTITIES = REGISTRY.quantities
OPERATORS = REGISTRY.operators
VERSION = REGISTRY.version
