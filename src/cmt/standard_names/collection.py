#! /usr/bin/env python
"""
A collection of StandardNames.
"""

from cmt.standard_names import StandardName


class Collection(set):
    """
    A set of CSDMS standard names.
    """
    def __init__(self, *args):
        super(Collection, self).__init__()

        if len(args) == 0:
            pass
        elif len(args) == 1:
            for name in args[0]:
                self.add(name)
        else:
            raise TypeError('Collection expected at most 1 argument, got %d' % len(args))

    def add(self, name):
        """
        Add a standard name to the collection, converting to StandardName if
        necessary.
        """
        if isinstance(name, StandardName):
            super(Collection, self).add(name)
        else:
            super(Collection, self).add(StandardName(name))

    def unique_names(self):
        """
        The unique names of a collection.
        """
        return set([str(n) for n in self])

    def unique_objects(self):
        """
        The unique object names of a collection.
        """
        objects = set()
        for name in self:
            objects.add(name.object())
        return objects

    def unique_quantities(self):
        """
        The unique quantity names of a collection.
        """
        quantities = set()
        for name in self:
            quantities.add(name.quantity())
        return quantities

    def unique_operators(self):
        """
        The unique operation names of a collection.
        """
        ops = set()
        for name in self:
            for operator in name.operators():
                ops.add(operator)
        return ops
