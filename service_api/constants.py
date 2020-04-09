import os
import sys
import json


def get_pg_host():
    if os.getenv('DOCK_ENV'):
        return 'mydb'
    return 'localhost'


def get_port(app_name):
    while 'test' in os.getcwd():
        os.chdir('..')
    with open('port_config.json', 'r') as f:
        data = json.load(f)
        return data[app_name]


if 'test' in str(sys.argv[0]):
    DB_CONFIG = {
        'host': get_pg_host(),
        'user': 'admin',
        'password': 'admin',
        'database': 'test_db'
    }
else:
    DB_CONFIG = {
        'host': get_pg_host(),
        'user': 'admin',
        'password': 'admin',
        'database': 'warehouse'
    }


BASIC_DB_CONFIG = {
    'host': get_pg_host(),
    'user': 'postgres',
    'password': 'admin',
    'database': 'postgres'
}


DEFAULT_SERVICE_NAME = "warehouse"
