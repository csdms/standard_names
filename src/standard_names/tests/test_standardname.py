#!/usr/bin/env python
"""
Unit tests for standard_names.StandardName
"""

import unittest

from standard_names import StandardName, BadNameError


class TestStandardName(unittest.TestCase):
    """
    Unit tests for standard_names.StandardName class.
    """
    def test_create(self):
        """
        Test class creation.
        """
        name = StandardName('air__temperature')

        self.assertEqual(name.name, 'air__temperature')

    def test_bad_name(self):
        """
        Try to create an invalid name.
        """
        with self.assertRaises(BadNameError):
            StandardName('air_temperature')

        with self.assertRaises(BadNameError):
            StandardName('air___temperature')

        with self.assertRaises(BadNameError):
            StandardName('Air__Temperature')

        with self.assertRaises(BadNameError):
            StandardName('_air__temperature')

        with self.assertRaises(BadNameError):
            StandardName('air__temperature_')

        with self.assertRaises(BadNameError):
            StandardName('air__temperature__0')

        with self.assertRaises(BadNameError):
            StandardName('0_air__temperature')

    def test_get_object(self):
        """
        Retrieve an object from a standard name.
        """
        name = StandardName('air__temperature')
        self.assertEqual(name.object, 'air')

    def test_get_quantity(self):
        """
        Retrieve a quantity from a standard name.
        """
        name = StandardName('air__temperature')
        self.assertEqual(name.quantity, 'temperature')

    def test_get_empty_operator(self):
        """
        Retrieve an operator from a standard name.
        """
        name = StandardName('air__temperature')

        self.assertTupleEqual(name.operators, ())

    def test_get_one_operator(self):
        """
        Retrieve an operator from a standard name.
        """
        name = StandardName('air__log_of_temperature')

        self.assertTupleEqual(name.operators, ('log', ))

    def test_get_multiple_operators(self):
        """
        Retrieve an operator from a standard name.
        """
        name = StandardName('air__mean_of_log_of_temperature')
        self.assertTupleEqual(name.operators, ('mean', 'log'))

    def test_compare_names(self):
        """
        Compare a names
        """
        name = StandardName('air__temperature')

        self.assertTrue(name == StandardName('air__temperature'))
        self.assertTrue(name != StandardName('water__temperature'))

    def test_compare_name_to_str(self):
        """
        Compare a name to a string
        """
        name = StandardName('air__temperature')

        self.assertTrue(name == 'air__temperature')
        self.assertTrue(name != 'water__temperature')

        self.assertFalse(name != 'air__temperature')
        self.assertFalse(name == 'water__temperature')

    def test_lt_name_to_str(self):
        """
        Names are ordered alphabetically
        """
        air = StandardName('air__temperature')
        water = StandardName('water__temperature')

        self.assertTrue(air < 'water__temperature')
        self.assertTrue(air < water)
        self.assertFalse('water__temperature' < air)
        self.assertFalse(water < air)

    def test_gt_name_to_str(self):
        """
        Names are ordered alphabetically
        """
        air = StandardName('air__temperature')
        water = StandardName('water__temperature')

        self.assertFalse(air > 'water__temperature')
        self.assertFalse(air > water)
        self.assertTrue('water__temperature' > air)
        self.assertTrue(water > air)

    def test_hash(self):
        """
        Hash based on string
        """
        a_bunch_of_names = set()

        a_bunch_of_names.add(StandardName('air__temperature'))
        a_bunch_of_names.add(StandardName('water__temperature'))

        self.assertEqual(len(a_bunch_of_names), 2)

        a_bunch_of_names.add(StandardName('air__temperature'))

        self.assertEqual(len(a_bunch_of_names), 2)

        self.assertTrue('air__temperature' in a_bunch_of_names)
        self.assertTrue('water__temperature' in a_bunch_of_names)
        self.assertTrue(StandardName('air__temperature') in a_bunch_of_names)

        self.assertFalse('surface__temperature' in a_bunch_of_names)

if __name__ == '__main__':
    unittest.main()
