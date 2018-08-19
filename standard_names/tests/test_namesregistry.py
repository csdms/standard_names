#!/usr/bin/env python
"""Unit tests for standard_names.NamesRegistry."""
import pytest
from six import string_types
from six.moves import StringIO

from standard_names import NamesRegistry, StandardName, BadNameError, BadRegistryError
from standard_names.registry import load_names_from_txt


def test_load_names_bad_onerror():
    with pytest.raises(ValueError):
        load_names_from_txt("dummy_arg", onerror="bad_value")


def test_load_names_bad_name_pass():
    file_like = StringIO("air__temperature\nwater_temperature")
    names = load_names_from_txt(file_like, onerror="pass")
    assert names == {"air__temperature"}


def test_load_names_bad_name_raise():
    file_like = StringIO("air__temperature\nwater_temperature")
    with pytest.raises(BadRegistryError, match="Registry contains invalid names"):
        load_names_from_txt(file_like, onerror="raise")

    file_like = StringIO("air__temperature\nwater_temperature")
    try:
        load_names_from_txt(file_like, onerror="raise")
    except BadRegistryError as error:
        assert error.names == ("water_temperature",)


def test_create_full():
    """Test creating default registry."""
    nreg = NamesRegistry()
    assert len(nreg) > 0


def test_create_empty():
    """Test creating default registry."""
    nreg = NamesRegistry(None)
    assert len(nreg) == 0


def test_create_with_too_many_args():
    """Test creating a registry with too many arguments."""
    with pytest.raises(ValueError):
        NamesRegistry("file1", "file2")


def test_create_with_file_like():
    """Test creating a registry from a file_like object."""
    file_like = StringIO("air__temperature")
    names = NamesRegistry(file_like)
    assert names.names == ("air__temperature",)

    file_like = StringIO("air__temperature")
    another_file_like = StringIO("water__temperature")
    names = NamesRegistry([file_like, another_file_like])
    assert isinstance(names.names, tuple)
    assert sorted(names.names) == ["air__temperature", "water__temperature"]


def test_create_with_from_path():
    """Test creating registry with from_path."""
    file_like = StringIO("air__temperature")
    names = NamesRegistry.from_path(file_like)
    assert names.names == ("air__temperature",)


def test_bad_name():
    """Try to add an invalid name."""
    nreg = NamesRegistry(None)
    with pytest.raises(BadNameError):
        nreg.add("air_temperature")


def test_add_string():
    """Add a string to the collection."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")

    assert StandardName("air__temperature") in nreg
    assert "air__temperature" in nreg
    assert len(nreg) == 1

    nreg.add("air__temperature")
    assert len(nreg) == 1


def test_collection_contains_names():
    """Make sure a NamesRegistry only contains StandardName objects."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    for name in nreg:
        assert isinstance(name, string_types)


def test_add_name():
    """Add a name to the collection."""
    nreg = NamesRegistry(None)
    nreg.add(StandardName("air__temperature"))

    assert StandardName("air__temperature") in nreg
    assert "air__temperature" in nreg


def test_unique_names():
    """List of unique names."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    assert len(nreg) == 2

    assert "air__temperature" in nreg
    assert "water__temperature" in nreg


def test_unique_objects():
    """List of unique objects."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    objs = nreg.objects

    assert len(objs) == 2
    assert "air" in objs
    assert "water" in objs


def test_unique_quantities():
    """List of unique quantities."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    quantities = nreg.quantities

    assert quantities == ("temperature",)


def test_unique_operators():
    """List of unique operators."""
    nreg = NamesRegistry(None)
    nreg.add("air__temperature")
    nreg.add("water__temperature")
    nreg.add("air__log_of_temperature")
    nreg.add("air__mean_of_log_of_temperature")

    operators = nreg.operators

    assert len(operators) == 2
    assert "log" in operators
    assert "mean" in operators
