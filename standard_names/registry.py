#! /usr/bin/env python
import os
import warnings
from glob import glob

from six import string_types

from .standardname import StandardName
from .error import BadNameError, BadRegistryError


def load_names_from_txt(file_like, onerror="raise"):
    """Load names from a text file.

    Parameters
    ----------
    file_like : file-like
        A file-like object that represents the contents of a text file
        (only a ``readline`` method need be available).
    onerror : {'raise', 'warn', 'pass'}
        What to do if a bad name is encountered in the file.

    Returns
    -------
    set of str
        The Standard Names read from the file.

    Examples
    --------
    >>> from six.moves import StringIO
    >>> import standard_names as csn
    >>> names = StringIO(\"\"\"
    ... air__temperature
    ... Water__Temperature
    ... \"\"\")
    >>> set_of_names = csn.registry.load_names_from_txt(names, onerror='warn')
    >>> [name.name for name in set_of_names]
    ['air__temperature']
    """
    if onerror not in ("pass", "raise", "warn"):
        raise ValueError("value for onerror keyword not understood")

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
        if onerror == "warn":
            for name in bad_names:
                warnings.warn("{name}: not a valid name".format(name=name))
        elif onerror == "raise":
            raise BadRegistryError(bad_names)

    return names


def _strict_version_or_raise(version_str):
    from distutils.version import StrictVersion

    if StrictVersion.version_re.match(version_str):
        return StrictVersion(version_str)
    else:
        raise ValueError("{version}: Not a version string".format(version=version_str))


def _get_latest_names_file(path=None, prefix="names-", suffix=".txt"):
    """Get the most recent version of a names file.

    Parameters
    ----------
    path : str, optional
        If given, the path to a folder holding names files. Otherwise,
        the default location within the *standard_names* package.
    prefix : str, optional
        The prefix for names-file glob.
    suffix : str, optional
        The suffix for names-file glob.

    Returns
    -------
    tuple of str
        Tuple of the name of the latest file and its version.

    Examples
    --------
    >>> import os
    >>> from standard_names.registry import _get_latest_names_file

    >>> fname, version = _get_latest_names_file()
    >>> os.path.basename(fname)
    'names-0.8.5.txt'
    >>> version
    '0.8.5'

    >>> _get_latest_names_file(prefix='garbage')
    (None, None)

    >>> _get_latest_names_file(prefix='names-0.8.3')
    (None, None)
    """
    data_dir = path or os.path.join(os.path.dirname(__file__), "data")

    name_glob = "{prefix}*{suffix}".format(prefix=prefix, suffix=suffix)
    data_file_pattern = os.path.join(data_dir, name_glob)
    files = [os.path.basename(file_) for file_ in glob(data_file_pattern)]

    newest = None
    for file in files:
        version_str = file[len(prefix) : -len(suffix)]
        try:
            version = _strict_version_or_raise(version_str)
        except ValueError:
            pass
        else:
            if newest is None or version > newest:
                newest = version

    if newest:
        version = str(newest)
        names_file = os.path.join(
            data_dir,
            "{prefix}{version}{suffix}".format(
                prefix=prefix, suffix=suffix, version=version
            ),
        )
        return names_file, version
    else:
        return None, None


class NamesRegistry(object):

    """A registry of CSDMS Standard Names.

    Parameters
    ----------
    paths : str or iterable of str, optional
        Name(s) of the data file(s) from which to read. If not given,
        use a default database. If ``None``, create an empty registry.
    version : str, optional
        The version of the names registry.
    
    Attributes
    ----------
    version
    names
    objects
    quantities
    operators

    Examples
    --------
    >>> from standard_names import NamesRegistry

    Get the default set of names.

    >>> registry = NamesRegistry()
    >>> len(registry) > 0
    True

    Create an empty registry and add a name to it.

    >>> registry = NamesRegistry(None)
    >>> len(registry)
    0
    >>> registry.add('air__temperature')
    >>> len(registry)
    1

    Use the ``names``, ``objects``, ``quantities``, and ``operators`` to
    get lists of each in the registry.

    >>> registry.names
    ('air__temperature',)
    >>> registry.objects
    ('air',)
    >>> registry.quantities
    ('temperature',)
    >>> registry.operators
    ()

    You can search the registry for names using the ``names_with``,
    ``match``, and ``search`` methods.

    Use ``names_with`` to look for names that contain a given string or
    strings.

    >>> registry.add('water__temperature')
    >>> sorted(registry.names_with('temperature'))
    ['air__temperature', 'water__temperature']
    >>> registry.names_with(['temperature', 'air'])
    ['air__temperature']

    Use ``match`` to match names using a glob-style pattern.

    >>> registry.match('air*')
    ['air__temperature']

    Use ``search`` to do a fuzzy search of the list.

    >>> registry.search('air__temp')
    ['air__temperature']
    """

    def __init__(self, *args, **kwds):
        if len(args) == 0:
            paths, version = _get_latest_names_file()
        elif len(args) == 1:
            paths, version = args[0], None
        else:
            raise ValueError("0 or 1 arguments expected")

        if paths is None:
            paths = []

        if isinstance(paths, string_types) or hasattr(paths, "readline"):
            paths = [paths]

        self._names = set()
        self._objects = set()
        self._quantities = set()
        self._operators = set()

        self._version = version or "0.0.0"

        for path in paths:
            if isinstance(path, string_types):
                with open(path, "r") as fp:
                    self._load(fp)
            else:
                self._load(path)

    def _load(self, file_like, onerror="raise"):
        for name in load_names_from_txt(file_like, onerror=onerror):
            self.add(name)

    @property
    def version(self):
        """The version of the names database.
        
        Returns
        -------
        str
            The registry version.
        """
        return self._version

    @property
    def names(self):
        """All names in the registry.
        
        Returns
        -------
        tuple of str
            All of the names in the registry.
        """
        return tuple(self._names)

    @property
    def objects(self):
        """All objects in the registry.
        
        Returns
        -------
        tuple of str
            All of the objects in the registry.
        """
        return tuple(self._objects)

    @property
    def quantities(self):
        """All quantities in the registry.
        
        Returns
        -------
        tuple of str
            All of the quantities in the registry.
        """
        return tuple(self._quantities)

    @property
    def operators(self):
        """All operators in the registry.
        
        Returns
        -------
        tuple of str
            All of the operators in the registry.
        """
        return tuple(self._operators)

    @classmethod
    def from_path(cls, path):
        """Create a new registry from a text file.

        Parameters
        ----------
        path : str
            Path to a text file of Standard Names.

        Returns
        -------
        NamesRegistry
            A newly-created registry filled with names from the file.
        """
        return cls(path)

    def add(self, name):
        """Add a name to the registry.

        Parameters
        ----------
        name : str
            A Standard Name.
        """
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
        """Search the registry for a name.

        Parameters
        ----------
        name : str
            Name to search for.

        Returns
        -------
        tuple of str
            Names that closely match the given name.
        """
        from difflib import get_close_matches

        return get_close_matches(name, self._names)

    def match(self, pattern):
        """Search the registry for names that match a pattern.

        Parameters
        ----------
        pattern : str
            Glob-style pattern with which to search the registry.

        Returns
        -------
        list of str
            List of names matching the pattern.
        """
        import re, fnmatch

        p = re.compile(fnmatch.translate(pattern))
        names = []
        for name in self._names:
            if p.match(name):
                names.append(name)
        return names

    def names_with(self, parts):
        """Search the registry for names containing words.

        Parameters
        ----------
        parts : str or iterable of str
            Word(s) to search for.

        Returns
        -------
        tuple of str
            Names from the registry that contains the given words.
        """
        if isinstance(parts, string_types):
            parts = (parts,)

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
