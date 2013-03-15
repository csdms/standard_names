#!/usr/bin/env python
"""
Unit tests for standard_names.StandardName
"""

import unittest

from standard_names import StandardName


class TestStandardName(unittest.TestCase):
    """
    Unit tests for standard_names.StandardName class.
    """
    def test_create(self):
        """
        Test class creation.
        """
        name = StandardName('air__temperature')

        self.assertEqual(name.name(), 'air__temperature')


if __name__ == '__main__':
    unittest.main()
