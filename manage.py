import argparse
import sys
import socket
import asyncio

from commands import runserver, InitDB
from service_api.utils.load_json_data import load_fixtures
from service_api.constants import DEFAULT_SERVICE_NAME


def parse_args(args):
    """Function for parsing arguments from command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parser_jl = subparsers.add_parser('load_json')
    group = parser_jl.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', dest='all', action='store_true')
    group.add_argument('-t', '--table', dest='table', nargs='+')
    return parser.parse_args(args=args)


def main(args=None):
    my_loop = asyncio.get_event_loop()
    my_loop.run_until_complete(InitDB(DEFAULT_SERVICE_NAME).create_db())

    parsed_args = parse_args(args or sys.argv[1:])

    if parsed_args.command == "load_json":
        load_fixtures(parsed_args)

    runserver()


if __name__ == '__main__':
    main()
