import sys


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


