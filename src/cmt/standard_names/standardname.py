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


_PREFIX_REGEX = '^[a-z]([a-z]|_(?!_))*'
#_PREFIX_REGEX = '^[a-z0-9]([a-z]|_(?!_))*'
_SUFFIX_REGEX ='[a-z0-9]([a-z]|_(?!_))*[a-z0-9]$' 
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
        Initialize a standard name.

        :name: String of the standard name
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
        Decompose a standard name into it's constituent parts (object,
        quantity, and operator).

        :name: String of the standard name
        :returns: A 3-tuple of (object, quantity, operator)
        """
        try:
            (object_part, quantity_clause) = name.split('__')
        except ValueError:
            raise BadNameError(name)

        (operators, quantity_part) = StandardName.decompose_quantity(
            quantity_clause)

        return (object_part, quantity_part, operators)

    @staticmethod
    def decompose_quantity(quantity_clause):
        """
        Decompose a quantity clause into operator and base quantity
        constituents. Because multiple operators can act on a quantity,
        the operators are given as a tuple regardless of the number of
        operators.

        :quantity_clause: Quantity as a string
        :returns: Tuple of (operators, base quantity)
        """
        quantity_parts = quantity_clause.split('_of_')
        quantity = quantity_parts[-1]
        operators = tuple(quantity_parts[:-1])

        return (operators, quantity)

    def name(self):
        """
        The full string of the standard name

        :returns: Standard name as a string
        """
        return self._name

    def object(self):
        """
        The object part of the standard name.

        :returns: Object name as a string
        """
        return self._object

    def quantity(self):
        """
        The quantity part of the standard name.

        :returns: Quantity name as a string
        """
        return self._quantity

    def operators(self):
        """
        The operator part of the standard name.

        :returns: Operator name as a string
        """
        return self._operators

    def __repr__(self):
        return 'StandardName(%s)' % self._name

    def __eq__(self, that):
        return self._name == str(that)

    def __ne__(self, that):
        return self._name != str(that)

    def __cmp__(self, that):
        return self._name == str(that)

    def __hash__(self):
        return hash(self._name)
