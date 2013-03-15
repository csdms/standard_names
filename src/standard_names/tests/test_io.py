#!/usr/bin/env python
"""
Unit tests for standard_names.io module
"""

import unittest
from StringIO import StringIO

from standard_names import (Collection, StandardName, BadNameError,
                            from_model_file)


_SINGLE_MODEL_FILE_STREAM = StringIO(
"""
%YAML 1.2
---
model name: topoflow
exchange items:
  - air__density
  - air__emissivity
...""")

_MULTIPLE_MODEL_FILE_STREAM = StringIO(
"""
%YAML 1.2
---
model name: topoflow
exchange items:
  - air__density
  - air__emissivity
---
model name: sedflux
exchange items:
  - air__density
  - water__temperature
...""")

_SINGLE_MODEL_FILE_STREAM_WITH_INTENT = StringIO(
"""
%YAML 1.2
---
model name: topoflow
exchange items:
  input:
    - air__density
  output:
    - air__density
    - air__emissivity
...""")

class TestStandardNameIO(unittest.TestCase):
    """
    Unit tests for standard_names.io module
    """
    def test_from_model_file(self):
        """
        Read from a YAML model file that contains one model.
        """
        names = from_model_file(_SINGLE_MODEL_FILE_STREAM)

        self.assertTrue('air__density' in names)
        self.assertTrue('air__emissivity' in names)
        self.assertEqual(len(names), 2)

    def test_from_multiple_model_file(self):
        """
        Read from a YAML model file that contains multiple models.
        """
        names = from_model_file(_MULTIPLE_MODEL_FILE_STREAM)

        self.assertTrue('air__density' in names)
        self.assertTrue('air__emissivity' in names)
        self.assertTrue('water__temperature' in names)
        self.assertEqual(len(names), 3)

    def test_from_model_file_with_intent(self):
        """
        Read from a YAML model file that contains one model but that indicates
        intent of variables.
        """
        names = from_model_file(_SINGLE_MODEL_FILE_STREAM_WITH_INTENT)

        self.assertTrue('air__density' in names)
        self.assertTrue('air__emissivity' in names)
        self.assertEqual(len(names), 2)


if __name__ == '__main__':
    unittest.main()
