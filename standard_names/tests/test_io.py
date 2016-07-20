#!/usr/bin/env python
"""Unit tests for standard_names.io module."""
from six.moves import StringIO

from nose.tools import assert_equal, assert_in

from standard_names import StandardName, BadNameError, from_model_file


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


def test_from_model_file():
    """Read from a YAML model file that contains one model."""
    names = from_model_file(_SINGLE_MODEL_FILE_STREAM)

    assert_in('air__density', names)
    assert_in('air__emissivity', names)
    assert_equal(len(names), 2)


def test_from_multiple_model_file():
    """Read from a YAML model file that contains multiple models."""
    names = from_model_file(_MULTIPLE_MODEL_FILE_STREAM)

    assert_in('air__density', names)
    assert_in('air__emissivity', names)
    assert_in('water__temperature', names)
    assert_equal(len(names), 3)


def test_from_model_file_with_intent():
    """
    Read from a YAML model file that contains one model but that indicates
    intent of variables.
    """
    names = from_model_file(_SINGLE_MODEL_FILE_STREAM_WITH_INTENT)

    assert_in('air__density', names)
    assert_in('air__emissivity', names)
    assert_equal(len(names), 2)
