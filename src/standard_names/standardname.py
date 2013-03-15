#! /usr/bin/env python
"""
StandardName class to hold a CSDMS standard name.
"""


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


class StandardName():
    """
    A CSDMS standard name.
    """
    def __init__(self, name):
        """
        Initialize a standard name.

        :name: String of the standard name
        """
        self._name = name
        
        (self._object,
         self._quantity,
         operator) = StandardName.decompose_name(name)

        if len(operator) > 0:
            self._operator = operator

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

        try:
            (operator_part, quantity_part) = quantity_clause.split('_of_')
        except ValueError:
            (operator_part, quantity_part) = ('', quantity_clause)

        return (object_part, quantity_part, operator_part)

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

    def operator(self):
        """
        The operator part of the standard name.

        :returns: Operator name as a string
        """
        return self._operator

    def __repr__(self):
        return 'StandardName(%s)' % self._name

    def __eq__(self, that):
        return self._name == that.name()

    def __cmp__(self, that):
        return self._name == that.name()

    def __hash__(self):
        return hash(self._name)
