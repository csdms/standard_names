#! /usr/bin/env python
"""
A collection of StandardNames.
"""

class Collection(set):
    """
    A set of CSDMS standard names.
    """
    def unique_names(self):
        """
        The unique names of a collection.
        """
        return set([n.name() for n in self])

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
            try:
                ops.add(name.operator())
            except AttributeError:
                pass
        return ops
