import re

STANDARD_NAME_REGEX = re.compile(
    r"""
    ^                           # Start of the string
    [a-z]+                      # Starts with one or more lowercase letters
    (?:                         # Start of a non-capturing group for subsequent parts
        [-~_]?                  # Optional separator: hyphen, tilde, or underscore
        [a-zA-Z0-9]+            # One or more alphanumeric characters
    )*                          # Zero or more repetitions of the group
    __                          # Double underscore separator
    [a-z]+                      # Another lowercase word
    (?:                         # Start of a non-capturing group for subsequent parts
        [-~_]?                  # Optional separator: hyphen, tilde, or underscore
        [a-zA-Z0-9]+            # One or more alphanumeric characters
    )*                          # Zero or more repetitions of the group
    $                           # End of the string
    """,
    re.VERBOSE,
)

_PATTERN = re.compile(
    r"""
    (?<!\w)                   # Negative look-behind for a non-word character
    [a-z]+                    # Starts with one or more lowercase letters
    (?:                       # Start of a non-capturing group for subsequent parts
        [-~_]?                # Optional separator: hyphen, tilde, or underscore
        [a-zA-Z0-9]+          # One or more alphanumeric characters
    )*                        # Zero or more repetitions of the group
    __                        # Double underscore separator
    [a-z]+                    # Another lowercase word
    (?:                       # Start of a non-capturing group for subsequent parts
        [-~_]?                # Optional separator: hyphen, tilde, or underscore
        [a-zA-Z0-9]+          # One or more alphanumeric characters
    )*                        # Zero or more repetitions of the group
    (?=\W|$)                  # Positive look-ahead for a space or end of string
    """,
    re.VERBOSE,
)


def findall(line: str) -> list[str]:
    return _PATTERN.findall(line.strip())
