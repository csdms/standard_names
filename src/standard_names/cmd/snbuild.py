#! /usr/bin/env python
"""
Example usage:
    snbuild data/models.yaml data/scraped.yaml \
            > standard_names/data/standard_names.yaml
"""

from standard_names.registry import NamesRegistry


def main(argv: tuple[str] | None = None) -> int:
    """Build a list of CSDMS standard names for YAML description files."""
    import argparse

    parser = argparse.ArgumentParser(
        "Scan a model description file for CSDMS standard names"
    )
    parser.add_argument(
        "file",
        nargs="*",
        type=argparse.FileType("r"),
        help="YAML file describing model exchange items",
    )

    args = parser.parse_args(argv)

    registry = NamesRegistry()
    for file in args.file:
        registry |= NamesRegistry(file)

    print(
        registry.dumps(
            format_="yaml",
            fields=("names", "objects", "quantities", "operators"),
            sort=True,
        )
    )

    return 0


if __name__ == "__main__":
    SystemExit(main())
