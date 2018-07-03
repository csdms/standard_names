#!/usr/bin/env python
"""Unit tests for standard_names.StandardName"""

from nose.tools import (
    assert_greater,
    assert_less,
    assert_equal,
    assert_not_equal,
    assert_in,
    assert_not_in,
    assert_is_instance,
    assert_tuple_equal,
    assert_raises,
    assert_false,
)

from standard_names import StandardName, BadNameError


def test_create():
    """Test class creation."""
    name = StandardName("air__temperature")

    assert_equal(name.name, "air__temperature")


def test_bad_name():
    """Try to create an invalid name."""
    with assert_raises(BadNameError):
        StandardName("air_temperature")

    with assert_raises(BadNameError):
        StandardName("air___temperature")

    with assert_raises(BadNameError):
        StandardName("Air__Temperature")

    with assert_raises(BadNameError):
        StandardName("_air__temperature")

    with assert_raises(BadNameError):
        StandardName("air__temperature_")

    with assert_raises(BadNameError):
        StandardName("air__temperature__0")

    with assert_raises(BadNameError):
        StandardName("0_air__temperature")


def test_get_object():
    """Retrieve an object from a standard name."""
    name = StandardName("air__temperature")
    assert_equal(name.object, "air")


def test_get_quantity():
    """Retrieve a quantity from a standard name."""
    name = StandardName("air__temperature")
    assert_equal(name.quantity, "temperature")


def test_get_empty_operator():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__temperature")

    assert_tuple_equal(name.operators, ())


def test_get_one_operator():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__log_of_temperature")

    assert_tuple_equal(name.operators, ("log",))


def test_get_multiple_operators():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__mean_of_log_of_temperature")
    assert_tuple_equal(name.operators, ("mean", "log"))


def test_compare_names():
    """Compare a names."""
    name = StandardName("air__temperature")

    assert_equal(name, StandardName("air__temperature"))
    assert_not_equal(name, StandardName("water__temperature"))


def test_compare_name_to_str():
    """Compare a name to a string."""
    name = StandardName("air__temperature")

    assert_equal(name, "air__temperature")
    assert_not_equal(name, "water__temperature")

    assert_false(name != "air__temperature")
    assert_false(name == "water__temperature")


def test_lt_name_to_str():
    """Names are ordered alphabetically."""
    air = StandardName("air__temperature")
    water = StandardName("water__temperature")

    assert_less(air, "water__temperature")
    assert_less(air, water)
    assert_false("water__temperature" < air)
    assert_false(water < air)


def test_gt_name_to_str():
    """Names are ordered alphabetically."""
    air = StandardName("air__temperature")
    water = StandardName("water__temperature")

    assert_false(air > "water__temperature")
    assert_false(air > water)
    assert_greater("water__temperature", air)
    assert_greater(water, air)


def test_hash():
    """Hash based on string."""
    a_bunch_of_names = set()

    a_bunch_of_names.add(StandardName("air__temperature"))
    a_bunch_of_names.add(StandardName("water__temperature"))

    assert_equal(len(a_bunch_of_names), 2)

    a_bunch_of_names.add(StandardName("air__temperature"))

    assert_equal(len(a_bunch_of_names), 2)

    assert_in("air__temperature", a_bunch_of_names)
    assert_in("water__temperature", a_bunch_of_names)
    assert_in(StandardName("air__temperature"), a_bunch_of_names)

    assert_not_in("surface__temperature", a_bunch_of_names)
