from __future__ import annotations

import argparse
import os
import sys

from standard_names._format import FORMATTERS
from standard_names._version import __version__
from standard_names.cli._scrape import scrape_names
from standard_names.cli._sql import as_sql_commands
from standard_names.cli._validate import validate_names
from standard_names.registry import NamesRegistry

VALID_FIELDS = {
    "op": "operators",
    "q": "quantities",
    "o": "objects",
    "n": "names",
}


class FatalError(RuntimeError):
    def __init__(self, msg: str):
        self._msg = msg

    def __str__(self) -> str:
        return self._msg


def main(argv: tuple[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"standard-names {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command")

    def _add_cmd(name: str, *, help: str) -> argparse.ArgumentParser:
        parser = subparsers.add_parser(name, help=help)
        parser.add_argument(
            "-v",
            "--verbose",
            action="count",
            help="Also emit status messages to stderr",
        )
        parser.add_argument(
            "--silent", action="store_true", help="Suppress status messages"
        )
        return parser

    build_parser = _add_cmd(
        "build", help="Scan a model description file for CSDMS standard names"
    )
    build_parser.add_argument(
        "file",
        nargs="*",
        type=argparse.FileType("r"),
        help="YAML file describing model exchange items",
    )
    build_parser.set_defaults(func=build)

    dump_parser = _add_cmd("dump", help="Dump known standard names")
    dump_parser.add_argument(
        "file", type=argparse.FileType("r"), nargs="*", help="Read names from a file"
    )
    dump_parser.add_argument(
        "--field",
        "-f",
        action="append",
        default=[],
        help="Fields to print",
        choices=VALID_FIELDS,
    )
    dump_parser.add_argument(
        "--sort", action=argparse.BooleanOptionalAction, help="Sort/don't sort names"
    )
    dump_parser.add_argument(
        "--format", choices=FORMATTERS, default="text", help="Output format"
    )
    dump_parser.set_defaults(func=dump)

    scrape_parser = _add_cmd("scrape", help="Scrape standard names from a file or URL")
    scrape_parser.add_argument(
        "file", nargs="*", metavar="FILE", help="URL or file to scrape"
    )
    scrape_parser.set_defaults(func=scrape)

    sql_parser = _add_cmd("sql", help="Build an sqlite database from a list of names")
    sql_parser.add_argument(
        "file", nargs="*", type=argparse.FileType("r"), help="List of names"
    )
    sql_parser.set_defaults(func=sql)

    validate_parser = _add_cmd("validate", help="Validate a list of standard names")
    validate_parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        nargs="*",
        help="Read names from a file",
    )
    validate_parser.set_defaults(func=validate)

    args = parser.parse_args(argv)

    try:
        return args.func(args)
    except FatalError as err:
        print(err, file=sys.stderr)
        return 1


def build(args: argparse.Namespace) -> int:
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


def dump(args: argparse.Namespace) -> int:
    fields = [VALID_FIELDS[field] for field in args.field]

    registry = NamesRegistry([])
    for file in args.file:
        registry |= NamesRegistry(file)
    print(registry.dumps(format_=args.format, sort=args.sort, fields=fields))

    return 0


def scrape(args: argparse.Namespace) -> int:
    registry = scrape_names(args.file)
    print(registry.dumps(format_="text", fields=("names",)))

    return 0


def sql(args: argparse.Namespace) -> int:
    registry = NamesRegistry()
    for file in args.file:
        registry |= NamesRegistry(file)

    print(as_sql_commands(registry))

    return 0


def validate(args: argparse.Namespace) -> int:
    invalid_names = set()
    for file in args.file:
        invalid_names |= validate_names(file)

    if invalid_names:
        print(os.linesep.join(invalid_names))

    return len(invalid_names)


if __name__ == "__main__":
    SystemExit(main())
