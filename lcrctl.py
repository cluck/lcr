#!/usr/bin/env python
# -*- codecs: utf-8 -*-

from __future__ import unicode_literals, print_function

import sys
import argparse
import fnmatch
import getpass

try:
    import psycopg2
except ImportError:
    psycopg2 = None

try:
    import peewee
except ImportError:
    peewee = None


DESCRIPTION = 'Leightweith Content Repository (LCR) Control Utility'

MODULES = {}

if psycopg2 is not None:
    MODULES["PostgreSQL"] = ("psycopg2", psycopg2.__version__)
else:
    MODULES["PostgresSQL"] = ('- Missing -', '')

if peewee is not None:
    MODULES['ORM'] = ('Peewee', peewee.__version__)
else:
    MODULES['ORM'] = ('- Missing -', '')

MODULES["Python"] = ("python", sys.version.split()[0])


def pg_server_version(args):
    try:
        conn = psycopg2.connect("dbname=postgres user={0}".format(args.username))
    except psycopg2.OperationalError as e:
        return e.message
    curs = conn.cursor()
    curs.execute('SELECT version FROM version()')
    vers = curs.fetchone()[0]
    return vers.split(',')[0]


def print_status(args):
    pg_server_ver = pg_server_version(args).rstrip()
    print()
    print("Server version:")
    print("  {0:20s} {1}".format("Database:", pg_server_ver))

    print()
    print("Modules installed:")
    for item, descr in MODULES.items():
        print("  {0:20s} {1} {2}".format(item + ":", *descr))
    return 2


def help(parser, args):
    parser.print_help()
    print_status(args)


def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        description=DESCRIPTION)

    parser.add_argument('--help', help='show this help message and exit')

    USERNAME = getpass.getuser()
    parser.add_argument('-U', '--username', metavar='USERNAME',
            help='username for request (default: {0})'.format(USERNAME), default=USERNAME)
    parser.add_argument('-h', '--host', metavar='HOSTNAME',
            help='database server host or socket directory (default: "local socket")',
            default='local socket')
    parser.add_argument('-p', '--port', metavar='PORT',
            help='database server port (default: "5432")', default=5432)

    args, unknowns = parser.parse_known_args()
    # Special
    args.password = None


    if args.help:
        return help(parser, args)

    print(DESCRIPTION)
    print_status(args)
    main2(args)


database_proxy = peewee.Proxy()

class BaseModel(peewee.Model):

    class Meta:
        database = database_proxy

class User(BaseModel):
    username = peewee.CharField()





def main2(args):

    db = peewee.PostgresqlDatabase(
        'postgres',
        user=args.username,
        password=args.password,
        host=args.host, port=args.port
    )
    database_proxy.initialize(db)
    print(db)


if __name__ == "__main__":
    sys.exit(main())
