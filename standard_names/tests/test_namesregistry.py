#!/usr/bin/env python
"""Unit tests for standard_names.NamesRegistry."""
from nose.tools import (assert_greater, assert_equal, assert_raises,
                        assert_in, assert_is_instance, assert_tuple_equal)
from six import string_types

from standard_names import NamesRegistry, StandardName, BadNameError


def test_create_full():
    """Test creating default registry."""
    nreg = NamesRegistry()
    assert_greater(len(nreg), 0)


def test_create_empty():
    """Test creating default registry."""
    nreg = NamesRegistry(None)
    assert_equal(len(nreg), 0)


def test_bad_name():
    """Try to add an invalid name."""
    nreg = NamesRegistry(None)
    with assert_raises(BadNameError):
        nreg.add('air_temperature')


def test_add_string():
    """Add a string to the collection."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')

    assert_in(StandardName('air__temperature'), nreg)
    assert_in('air__temperature', nreg)
    assert_equal(len(nreg), 1)

    nreg.add('air__temperature')
    assert_equal(len(nreg), 1)


def test_collection_contains_names():
    """Make sure a NamesRegistry only contains StandardName objects."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')
    nreg.add('water__temperature')

    for name in nreg:
        assert_is_instance(name, string_types)

def test_add_name():
    """Add a name to the collection."""
    nreg = NamesRegistry(None)
    nreg.add(StandardName('air__temperature'))

    assert_in(StandardName('air__temperature'), nreg)
    assert_in('air__temperature', nreg)


def test_unique_names():
    """List of unique names."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')
    nreg.add('water__temperature')

    assert_equal(len(nreg), 2)

    assert_in('air__temperature', nreg)
    assert_in('water__temperature', nreg)


def test_unique_objects():
    """List of unique objects."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')
    nreg.add('water__temperature')

    objs = nreg.objects

    assert_equal(len(objs), 2)
    assert_in('air', objs)
    assert_in('water', objs)


def test_unique_quantities():
    """List of unique quantities."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')
    nreg.add('water__temperature')

    quantities = nreg.quantities

    assert_tuple_equal(quantities, ('temperature', ))


def test_unique_operators():
    """List of unique operators."""
    nreg = NamesRegistry(None)
    nreg.add('air__temperature')
    nreg.add('water__temperature')
    nreg.add('air__log_of_temperature')
    nreg.add('air__mean_of_log_of_temperature')

    operators = nreg.operators

    assert_equal(len(operators), 2)
    assert_in('log', operators)
    assert_in('mean', operators)
