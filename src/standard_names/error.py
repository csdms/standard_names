from collections.abc import Iterable


class Error(Exception):

    """Base class for exceptions from this module."""

    pass


class BadNameError(Error):

    """Error to indicate a poorly-formed standard name."""

    def __init__(self, name: str):
        super().__init__()
        self._name = name

    def __str__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name


class BadRegistryError(Error):

    """Error to indicate a bad NamesRegistry."""

    def __init__(self, names: Iterable[str]):
        super().__init__()
        self._names = tuple(sorted(names))

    def __str__(self) -> str:
        return "Registry contains invalid names"

    @property
    def names(self) -> tuple[str, ...]:
        return self._names
