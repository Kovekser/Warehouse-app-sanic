import os
import sys
import json


if 'test' in str(sys.argv[0]):
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'postgres',
        'password': 'admin',
        'database': 'test_db'
    }
else:
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'admin',
        'password': 'admin',
        'database': 'warehouse'
    }


BASIC_DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'admin',
    'database': 'postgres'
}


DEFAULT_SERVICE_NAME = "warehouse"


def get_port(app_name):
    while 'test' in os.getcwd():
        os.chdir('..')
    with open('port_config.json', 'r') as f:
        data = json.load(f)
        return data[app_name]
