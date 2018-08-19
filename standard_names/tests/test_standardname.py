#!/usr/bin/env python
"""Unit tests for standard_names.StandardName"""
import pytest

from standard_names import StandardName, BadNameError


def test_create():
    """Test class creation."""
    name = StandardName("air__temperature")

    assert name.name == "air__temperature"


def test_bad_name():
    """Try to create an invalid name."""
    with pytest.raises(BadNameError):
        StandardName("air_temperature")

    with pytest.raises(BadNameError):
        StandardName("air___temperature")

    with pytest.raises(BadNameError):
        StandardName("Air__Temperature")

    with pytest.raises(BadNameError):
        StandardName("_air__temperature")

    with pytest.raises(BadNameError):
        StandardName("air__temperature_")

    with pytest.raises(BadNameError):
        StandardName("air__temperature__0")

    with pytest.raises(BadNameError):
        StandardName("0_air__temperature")


def test_get_object():
    """Retrieve an object from a standard name."""
    name = StandardName("air__temperature")
    assert name.object == "air"


def test_get_quantity():
    """Retrieve a quantity from a standard name."""
    name = StandardName("air__temperature")
    assert name.quantity == "temperature"


def test_get_empty_operator():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__temperature")

    assert name.operators == ()


def test_get_one_operator():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__log_of_temperature")

    assert name.operators == ("log",)


def test_get_multiple_operators():
    """Retrieve an operator from a standard name."""
    name = StandardName("air__mean_of_log_of_temperature")
    assert name.operators == ("mean", "log")


def test_compare_names():
    """Compare a names."""
    name = StandardName("air__temperature")

    assert name == StandardName("air__temperature")
    assert name != StandardName("water__temperature")


def test_compare_name_to_str():
    """Compare a name to a string."""
    name = StandardName("air__temperature")

    assert name == "air__temperature"
    assert name != "water__temperature"

    assert not (name != "air__temperature")
    assert not (name == "water__temperature")


def test_lt_name_to_str():
    """Names are ordered alphabetically."""
    air = StandardName("air__temperature")
    water = StandardName("water__temperature")

    assert air < "water__temperature"
    assert air < water
    assert not ("water__temperature" < air)
    assert not (water < air)


def test_gt_name_to_str():
    """Names are ordered alphabetically."""
    air = StandardName("air__temperature")
    water = StandardName("water__temperature")

    assert not (air > "water__temperature")
    assert not (air > water)
    assert "water__temperature" > air
    assert water > air


def test_hash():
    """Hash based on string."""
    a_bunch_of_names = set()

    a_bunch_of_names.add(StandardName("air__temperature"))
    a_bunch_of_names.add(StandardName("water__temperature"))

    assert len(a_bunch_of_names) == 2

    a_bunch_of_names.add(StandardName("air__temperature"))

    assert len(a_bunch_of_names) == 2

    assert "air__temperature" in a_bunch_of_names
    assert "water__temperature" in a_bunch_of_names
    assert StandardName("air__temperature") in a_bunch_of_names

    assert "surface__temperature" not in a_bunch_of_names
