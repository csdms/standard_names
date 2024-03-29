"""A CSDMS standard name."""
from __future__ import annotations

from typing import Any

from standard_names.error import BadNameError
from standard_names.regex import STANDARD_NAME_REGEX


def is_valid_name(name: str) -> bool:
    """Check if a string is a valid standard name.

    Parameters
    ----------
    name : str
        Standard name as a string

    Returns
    -------
    bool
        ``True`` if the string is a valid standard name
    """
    return bool(STANDARD_NAME_REGEX.match(name))


class StandardName:

    """A CSDMS standard name.

    Examples
    --------
    >>> import standard_names as csn
    >>> name = csn.StandardName('air__temperature')

    >>> name == 'air__temperature'
    True
    >>> repr(name)
    "StandardName('air__temperature')"

    >>> name.object = 'water'
    >>> repr(name)
    "StandardName('water__temperature')"

    >>> name.quantity = 'density'
    >>> repr(name)
    "StandardName('water__density')"

    >>> name.operators = ('max', )
    >>> repr(name)
    "StandardName('water__max_of_density')"

    >>> name.operators = 'min'
    >>> repr(name)
    "StandardName('water__min_of_density')"
    """

    re = STANDARD_NAME_REGEX

    def __init__(self, name: str):
        """Create a standard name object from a string.

        Parameters
        ----------
        name : str
            A Standard Name.
        """
        if not is_valid_name(name):
            raise BadNameError(name)

        self._name = name

        (self._object, self._quantity, self._operators) = StandardName.decompose_name(
            name
        )

    @staticmethod
    def decompose_name(name: str) -> tuple[str, str, tuple[str, ...]]:
        """Decompose a name into its parts.

        Decompose the *name* standard name string into it's constituent
        parts (object, quantity, and operator). Returns a tuple of
        (object, quantity, operator) where object and quantitiy are strings,
        and operator is itself a tuple of strings (or empty).

        Parameters
        ----------
        name : str
            A CSDMS Standard Name.

        Returns
        -------
        tuple of str
            The parts of a name as ``(object, quantity, operators)``

        Examples
        --------
        >>> import standard_names as csn
        >>> name = 'atmosphere_air__elevation_angle_of_gradient_of_temperature'
        >>> csn.StandardName.decompose_name(name)
        ('atmosphere_air', 'temperature', ('elevation_angle', 'gradient'))

        >>> try:
        ...     StandardName.decompose_name('air_temperature')
        ... except BadNameError:
        ...     pass
        """
        try:
            (object_part, quantity_clause) = name.split("__")
        except ValueError as error:
            raise BadNameError(name) from error

        (operators, quantity_part) = StandardName.decompose_quantity(quantity_clause)

        return object_part, quantity_part, operators

    @staticmethod
    def compose_name(
        object: str, quantity: str, operators: tuple[()] | tuple[str, ...] = ()
    ) -> str:
        """Create a string from the parts of StandardName.

        Parameters
        ----------
        object : str
            An StandardName object.
        quantity : str
            An StandardName quantity.
        operators : iterable of str, optional
            Operators applied to the quantity.

        Returns
        -------
        str
            The standard name composed of the given elements.

        Examples
        --------
        >>> import standard_names as csn
        >>> name = 'atmosphere_air__elevation_angle_of_gradient_of_temperature'
        >>> parts = csn.StandardName.decompose_name(name)
        >>> csn.StandardName.compose_name(*parts) == name
        True
        >>> csn.StandardName.compose_name('air', 'temperature')
        'air__temperature'
        """
        operator = "_of_".join(operators)
        if len(operator) > 0:
            quantity = "_of_".join([operator, quantity])

        return "__".join((object, quantity))

    @staticmethod
    def decompose_quantity(quantity_clause: str) -> tuple[tuple[str, ...], str]:
        """Decompose a quantity into operators and quantities.

        Decompose the *quantity_clause* string into operator and base
        quantity constituents. Because multiple operators can act on a
        quantity, the operators are given as a tuple regardless of the
        number of operators actually present. Returns the parts of the
        quantity as a tuple of (operators, base_quantity)

        Parameters
        ----------
        quantity_clause : str
            A CSDMS Standard Name quantity.

        Returns
        -------
        tuple of str
            The parts of the quantity as ``(operators, quantity)``.
        """
        quantity_parts = quantity_clause.split("_of_")
        quantity = quantity_parts[-1]
        operators = tuple(quantity_parts[:-1])

        return operators, quantity

    @property
    def name(self) -> str:
        """The full standard name as a string."""
        return self._name

    @property
    def object(self) -> str:
        """The object part of the standard name."""
        return self._object

    @object.setter
    def object(self, value: str) -> None:
        self._object = value
        self._name = StandardName.compose_name(
            self.object, self.quantity, self.operators
        )

    @property
    def quantity(self) -> str:
        """The quantity part of the standard name."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: str) -> None:
        self._quantity = value
        self._name = StandardName.compose_name(
            self.object, self.quantity, self.operators
        )

    @property
    def operators(self) -> tuple[str, ...]:
        """The operator part of the standard name."""
        return self._operators

    @operators.setter
    def operators(self, value: str | tuple[str, ...]) -> None:
        if isinstance(value, str):
            value = (value,)
        self._operators = value
        self._name = StandardName.compose_name(
            self.object, self.quantity, self.operators
        )

    def __repr__(self) -> str:
        return "StandardName(%r)" % self.name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, that: Any) -> bool:
        return self.name == str(that)

    def __ne__(self, that: Any) -> bool:
        return self.name != str(that)

    def __lt__(self, that: Any) -> bool:
        return self.name < str(that)

    def __gt__(self, that: Any) -> bool:
        return self.name > str(that)

    def __cmp__(self, that: Any) -> bool:
        return self.name == str(that)

    def __hash__(self) -> int:
        return hash(self.name)
