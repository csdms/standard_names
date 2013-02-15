#! /usr/bin/env python

class Error (Exception):
    pass
class BadNameError (Error):
    def __init__ (self, name):
        self._name = name
    def __str__ (self):
        return self._name

class StandardName ():
    def __init__ (self, name):
        self._name = name
        
        (self._object,
         self._quantity,
         operator) = StandardName.decompose_name (name)

        if len (operator) > 0:
            self._operator = operator

    @staticmethod
    def decompose_name (name):
        try:
            (object, quantity) = name.split ('__')
        except ValueError:
            raise BadNameError (name)

        try:
            (op, q) = quantity.split ('_of_')
        except ValueError:
            operator = ''
        else:
            operator = op
            quantity = q

        return (object, quantity, operator)

    def name (self):
        return self._name
    def object (self):
        return self._object
    def quantity (self):
        return self._quantity
    def operator (self):
        return self._operator

    def __repr__ (self):
        return 'StandardName (%s)' % self._name

    def __eq__ (self, that):
        return self._name == that._name

    def __cmp__ (self, that):
        return self._name == that._name

    def __hash__ (self):
        return hash (self._name)

