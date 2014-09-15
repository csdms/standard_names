#! /usr/bin/env python
"""
StandardName class to hold a CSDMS standard name.
"""

import re


class Error(Exception):
    """Base class for exceptions from this module."""
    pass


class BadNameError(Error):
    """
    Error to indicate a poorly-formed standard name.
    """
    def __init__(self, name):
        super(BadNameError, self).__init__()
        self._name = name

    def __str__(self):
        return self._name


_PREFIX_REGEX = '^[a-z]([a-zA-Z0-9-]|_(?!_))*'
#_PREFIX_REGEX = '^[a-z0-9]([a-z]|_(?!_))*'
_SUFFIX_REGEX = '[a-z0-9]([a-z0-9-]|_(?!_))*[a-z0-9]$'
STANDARD_NAME_REGEX = re.compile(
    _PREFIX_REGEX + '(__)' + _SUFFIX_REGEX
)
#    '^[a-z][a-z0-9_]*[a-z0-9](__)[a-z0-9][a-z0-9_]*[a-z0-9]$'


def is_valid_name(name):
    """
    Check if a string is a valid standard name.

    :name: Standard name as a string

    :returns: True if the string is a valid standard name
    """
    return bool(STANDARD_NAME_REGEX.match(name))


class StandardName(str):
    """
    A CSDMS standard name.
    """
    def __init__(self, name):
        """
        Initialize a standard name object from the string, *name*.
        """
        if not is_valid_name(name):
            raise BadNameError(name)

        super(StandardName, self).__init__(name)

        self._name = name
        
        (self._object,
         self._quantity,
         self._operators) = StandardName.decompose_name(name)

    @staticmethod
    def decompose_name(name):
        """
        Decompose the *name* standard name string into it's constituent
        parts (object, quantity, and operator). Returns a tuple of
        (object, quantity, operator) where object and quantitiy are strings,
        and operator is itself a tuple of strings (or empty).
        """
        try:
            (object_part, quantity_clause) = name.split('__')
        except ValueError:
            raise BadNameError(name)

        (operators, quantity_part) = StandardName.decompose_quantity(
            quantity_clause)

        return object_part, quantity_part, operators

    def _compose_name(self):
        """
        Create a string from the parts of StandardName.
        """
        operator = '_of_'.join(self._operators)
        if len(operator) > 0:
            quantity = '_of_'.join([operator, self._quantity])
        else:
            quantity = self._quantity

        return self._object + '__' + quantity

    @staticmethod
    def decompose_quantity(quantity_clause):
        """
        Decompose the *quantity_clause* string into operator and base
        quantity constituents. Because multiple operators can act on a
        quantity, the operators are given as a tuple regardless of the
        number of operators actually present. Returns the parts of the
        quantity as a tuple of (operators, base_quantity)
        """
        quantity_parts = quantity_clause.split('_of_')
        quantity = quantity_parts[-1]
        operators = tuple(quantity_parts[:-1])

        return operators, quantity

    @property
    def name(self):
        """
        The full standard name as a string.
        """
        #return self._name
        return str(self)

    #@name.setter
    #def name(self, value):
    #    self._name = value

    @property
    def object(self):
        """
        The object part of the standard name.

        :returns: Object name as a string
        """
        return self._object

    @object.setter
    def object(self, value):
        self._object = value

    @property
    def quantity(self):
        """
        The quantity part of the standard name.

        :returns: Quantity name as a string
        """
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        self._quantity = value

    @property
    def operators(self):
        """
        The operator part of the standard name.

        :returns: Operator name as a string
        """
        return self._operators

    @operators.setter
    def operators(self, value):
        self._operators = value

    def __repr__(self):
        return 'StandardName(%r)' % self.name

    def __str__(self):
        return self._compose_name()

    def __eq__(self, that):
        return self.name == str(that)

    def __ne__(self, that):
        return self.name != str(that)

    def __cmp__(self, that):
        return self.name == str(that)

    def __hash__(self):
        return hash(self.name)
