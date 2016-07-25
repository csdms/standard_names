#! /usr/bin/env python


class Error(Exception):

    """Base class for exceptions from this module."""

    pass


class BadNameError(Error):

    """Error to indicate a poorly-formed standard name."""

    def __init__(self, name):
        super(BadNameError, self).__init__()
        self._name = name

    def __str__(self):
        return self._name

    @property
    def name(self):
        return self._name


class BadRegistryError(Error):

    """Error to indicate a bad NamesRegistry."""

    def __init__(self, names):
        super(BadRegistryError, self).__init__()
        self._names = names

    def __str__(self):
        return "Registry contains invalid names"

    @property
    def names(self):
        return tuple(self._names)


class BadIntentError(Error):

    """Error to indicate a bad key for intent."""

    def __init__(self, key, valid_keys):
        super(BadIntentError, self).__init__()
        self._key = key
        self._valid_keys = valid_keys

    def __str__(self):
        return '%s: Should be one of %s' % (self._key,
                                            ','.join(self._valid_keys))


