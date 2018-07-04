#! /usr/bin/env python
from __future__ import print_function

import os

from ..utilities import FORMATTERS
from ..registry import NamesRegistry


_NAMES_SCHEMA = """
create table names (
    id       integer primary key,
    name     text,
    unique(name)
);
create table objects (
    id       integer primary key,
    name     text,
    unique(name)
);
create table quantities (
    id       integer primary key,
    name     text,
    unique(name)
);
create table operators (
    id       integer primary key,
    name     text,
    unique(name)
);
""".strip()


def as_sql_commands(names, newline=None):
    """Create an sql database from a NamesRegistry.

    Parameters
    ----------
    names : NamesRegistry
        A collection of CSDMS Standard Names.
    newline : str, optional
        Newline character to use for output.

    Returns
    -------
    str
        The SQL commands to create the database.

    Examples
    --------
    >>> import standard_names as csn
    >>> names = csn.NamesRegistry(None)
    >>> names.add('air__temperature')
    >>> print(csn.cmd.snsql.as_sql_commands(names, newline='\\n'))
    ...     # doctest: +REPORT_UDIFF
    BEGIN TRANSACTION;
    CREATE TABLE names (
        id       integer primary key,
        name     text,
        unique(name)
    );
    INSERT INTO "names" VALUES(1,'air__temperature');
    CREATE TABLE objects (
        id       integer primary key,
        name     text,
        unique(name)
    );
    INSERT INTO "objects" VALUES(1,'air');
    CREATE TABLE operators (
        id       integer primary key,
        name     text,
        unique(name)
    );
    CREATE TABLE quantities (
        id       integer primary key,
        name     text,
        unique(name)
    );
    INSERT INTO "quantities" VALUES(1,'temperature');
    COMMIT;
    """
    newline = newline or os.linesep

    from contextlib import closing
    from sqlite3 import connect

    with closing(connect(":memory:")) as db:
        db.cursor().executescript(_NAMES_SCHEMA)

        c = db.cursor()

        for name in names.names:
            c.execute("INSERT INTO names(name) VALUES ('%s');" % name)
        for name in names.objects:
            c.execute("INSERT INTO objects(name) VALUES ('%s');" % name)
        for name in names.quantities:
            c.execute("INSERT INTO quantities(name) VALUES ('%s');" % name)
        for name in names.operators:
            c.execute("INSERT INTO operators(name) VALUES ('%s');" % name)
        db.commit()

        commands = newline.join(db.iterdump())

    return commands


def main():
    """
    Build a database of CSDMS standard names from a list.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Build an sqlite database from a list of names"
    )
    parser.add_argument(
        "file", nargs="+", type=argparse.FileType("r"), help="List of names"
    )
    args = parser.parse_args()

    names = NamesRegistry(args.file)
    return as_sql_commands(names)


def run():
    print(main())
