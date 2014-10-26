#! /usr/bin/env python

import os

from .. import (from_model_file, FORMATTERS, Collection)
from ..io import from_list_file


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


def as_sql_commands(names):
    from contextlib import closing
    from sqlite3 import connect

    with closing(connect(':memory:')) as db:
        db.cursor().executescript(_NAMES_SCHEMA)

        c = db.cursor()

        for name in names.names():
            c.execute("INSERT INTO names(name) VALUES ('%s');" % name)
        for name in names.objects():
            c.execute("INSERT INTO objects(name) VALUES ('%s');" % name)
        for name in names.quantities():
            c.execute("INSERT INTO quantities(name) VALUES ('%s');" % name)
        for name in names.operators():
            c.execute("INSERT INTO operators(name) VALUES ('%s');" % name)
        db.commit()

        commands = os.linesep.join(db.iterdump())

    return commands


def main():
    """
    Build a database of CSDMS standard names from a list.
    """
    import argparse

    parser = argparse.ArgumentParser(
        description='Build an sqlite database from a list of names')
    parser.add_argument('file', nargs='+', type=argparse.FileType('r'),
                        help='List of names')
    args = parser.parse_args()

    names = Collection()
    for model_file in args.file:
        names |= from_list_file(model_file)

    print as_sql_commands(names)


if __name__ == '__main__':
    main()
