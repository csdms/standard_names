#!/usr/bin/env python
"""Unit tests for standard_names.NamesRegistry."""
from io import StringIO

import pytest

from standard_names.error import BadNameError
from standard_names.error import BadRegistryError
from standard_names.registry import NamesRegistry
from standard_names.registry import load_names_from_txt
from standard_names.standardname import StandardName


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
    nreg = NamesRegistry.from_latest()
    assert len(nreg) > 0


def test_create_empty():
    """Test creating default registry."""
    nreg = NamesRegistry()
    assert len(nreg) == 0


def test_create_with_file_like():
    """Test creating a registry from a file_like object."""
    from itertools import chain

    file_like = StringIO("air__temperature")
    names = NamesRegistry(file_like)
    assert names.names == ("air__temperature",)

    file_like = StringIO("air__temperature")
    another_file_like = StringIO("water__temperature")
    # names = NamesRegistry([file_like, another_file_like])
    names = NamesRegistry(chain(file_like, another_file_like))
    assert isinstance(names.names, tuple)
    assert sorted(names.names) == ["air__temperature", "water__temperature"]


def test_create_with_from_path(tmpdir):
    """Test creating registry with from_path."""
    file_like = StringIO("air__temperature")
    names = NamesRegistry(file_like)
    assert names.names == ("air__temperature",)

    with tmpdir.as_cwd():
        with open("names.txt", "w") as fp:
            fp.write("air__temperature")
        names = NamesRegistry.from_path("names.txt")
        assert names.names == ("air__temperature",)


def test_bad_name():
    """Try to add an invalid name."""
    nreg = NamesRegistry()
    with pytest.raises(BadNameError):
        nreg.add("air_temperature")


def test_add_string():
    """Add a string to the collection."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")

    assert StandardName("air__temperature") in nreg
    assert "air__temperature" in nreg
    assert len(nreg) == 1

    nreg.add("air__temperature")
    assert len(nreg) == 1


def test_collection_contains_names():
    """Make sure a NamesRegistry only contains StandardName objects."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    for name in nreg:
        assert isinstance(name, str)


def test_add_name():
    """Add a name to the collection."""
    nreg = NamesRegistry()
    nreg.add(StandardName("air__temperature"))

    assert StandardName("air__temperature") in nreg
    assert "air__temperature" in nreg


def test_unique_names():
    """List of unique names."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    assert len(nreg) == 2

    assert "air__temperature" in nreg
    assert "water__temperature" in nreg


def test_unique_objects():
    """List of unique objects."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    objs = nreg.objects

    assert len(objs) == 2
    assert "air" in objs
    assert "water" in objs


def test_unique_quantities():
    """List of unique quantities."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")
    nreg.add("water__temperature")

    quantities = nreg.quantities

    assert quantities == ("temperature",)


def test_unique_operators():
    """List of unique operators."""
    nreg = NamesRegistry()
    nreg.add("air__temperature")
    nreg.add("water__temperature")
    nreg.add("air__log_of_temperature")
    nreg.add("air__mean_of_log_of_temperature")

    operators = nreg.operators

    assert len(operators) == 2
    assert "log" in operators
    assert "mean" in operators
