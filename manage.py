import argparse
import sys
import os

from service_api.application import create_app
from service_api.utils.json_loader import JsonLoader

def parse_args(args):
    """Function for parsing arguments from command line"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    parser_jl = subparsers.add_parser('load_json')
    group = parser_jl.add_mutually_exclusive_group(required=True)
    group.add_argument('-a', '--all', dest='all', action='store_true')
    group.add_argument('-t', '--table', dest='table', nargs='+')
    # print(parser.parse_args(args=args))
    return parser.parse_args(args=args)

def fixtures_path(file=False):
    """
    Function for getting abs path to JSON file to be opened:
    depending on flag "file" returns path to fixtures folder
    or to the file.json
    """
    if file:
        json_path = os.path.abspath('/'.join((os.getcwd(), 'fixtures', file)))
    else:
        json_path = os.path.abspath('/'.join((os.getcwd(), 'fixtures')))
    return json_path


def json_exists(file_name):
    """Function validating if JSON file for requested table in DB exists"""
    if os.path.exists(file_name):
        return file_name
    else:
        raise FileNotFoundError


def main(args=None):
    parsed_args = parse_args(args or sys.argv[1:])

    if parsed_args.command == "load_json":
        if parsed_args.all:
            file_list = [fixtures_path(f) for f in os.listdir(fixtures_path())]
        else:
            file_list = [fixtures_path(f) for f in parsed_args.table]
        # print(file_list)
        data = [JsonLoader(json_exists(f)).loaded_json for f in file_list]  #list of generators
        print(data)
        print(next(data[0]))

    create_app()


if __name__ == '__main__':
    main()

