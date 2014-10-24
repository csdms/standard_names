#!/usr/bin/env python
"""
Unit tests for standard_names.Collection
"""

import unittest

from standard_names import Collection, StandardName, BadNameError


class TestStandardNameCollection(unittest.TestCase):
    """
    Unit tests for standard_names.Collection class.
    """
    def test_create(self):
        """
        Test class creation.
        """
        collection = Collection()

        self.assertEqual(len(collection), 0)

    def test_bad_name(self):
        """
        Try to add an invalid name.
        """
        collection = Collection()
        with self.assertRaises(BadNameError):
            collection.add('air_temperature')

    def test_add_string(self):
        """
        Add a string to the collection.
        """
        collection = Collection()
        collection.add('air__temperature')

        self.assertTrue(StandardName('air__temperature') in collection)
        self.assertTrue('air__temperature' in collection)

        self.assertEqual(len(collection), 1)

        collection.add('air__temperature')
        self.assertEqual(len(collection), 1)

    def test_collection_contains_names(self):
        """
        Make sure a Collection only contains StandardName objects.
        """
        collection = Collection(['air__temperature',
                                 'water__temperature'])
        for name in collection:
            self.assertTrue(type(name) is StandardName)

        collection = Collection()
        collection.add('air__temperature')
        collection.add('water__temperature')
        for name in collection:
            self.assertTrue(type(name) is StandardName)

    def test_add_name(self):
        """
        Add a name to the collection.
        """
        collection = Collection()
        collection.add(StandardName('air__temperature'))
        self.assertTrue(StandardName('air__temperature') in collection)
        self.assertTrue('air__temperature' in collection)

    def test_create_with_strings(self):
        """
        Add a list of strings to the collection.
        """
        collection = Collection(['air__temperature', 'water__temperature'])
        self.assertEqual(len(collection), 2)

        self.assertTrue('air__temperature' in collection)
        self.assertTrue('water__temperature' in collection)

    def test_create_with_names(self):
        """
        Add a list of names to the collection.
        """
        collection = Collection([StandardName('air__temperature'),
                                 StandardName('water__temperature')])
        self.assertEqual(len(collection), 2)

        self.assertTrue('air__temperature' in collection)
        self.assertTrue('water__temperature' in collection)

    def test_unique_names(self):
        """
        List of unique names.
        """
        collection = Collection(['air__temperature', 'water__temperature'])

        names = collection.names()

        self.assertEqual(len(names), 2)
        self.assertTrue('air__temperature' in names)
        self.assertTrue('water__temperature' in names)

    def test_unique_objects(self):
        """
        List of unique objects.
        """
        collection = Collection(['air__temperature', 'water__temperature'])

        objs = collection.objects()

        self.assertEqual(len(objs), 2)
        self.assertTrue('air' in objs)
        self.assertTrue('water' in objs)

    def test_unique_quantities(self):
        """
        List of unique quantities.
        """
        collection = Collection(['air__temperature', 'water__temperature'])

        quantities = collection.quantities()

        self.assertEqual(len(quantities), 1)
        self.assertTrue('temperature' in quantities)

    def test_unique_operators(self):
        """
        List of unique operators.
        """
        collection = Collection(['air__temperature',
                                 'water__temperature',
                                 'air__log_of_temperature',
                                 'air__mean_of_log_of_temperature',
                                ])

        operators = collection.operators()

        self.assertEqual(len(operators), 2)
        self.assertTrue('log' in operators)
        self.assertTrue('mean' in operators)


if __name__ == '__main__':
    unittest.main()
