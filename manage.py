import argparse
import sys
import os

from commands import runserver
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path, get_tab_name


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
    parsed_args = parse_args(args or sys.argv[1:])

    if parsed_args.command == "load_json":
        if parsed_args.all:
            file_list = [get_abs_path(f) for f in os.listdir(get_abs_path())]
        else:
            file_list = [get_abs_path(f) for f in parsed_args.table]
        print(file_list)
        data = {get_tab_name(f): JsonLoader(f).loaded_json for f in file_list}  # dict of generators {tab_name: Gen}
        # TODO insert data to database

    runserver()


if __name__ == '__main__':
    main()
