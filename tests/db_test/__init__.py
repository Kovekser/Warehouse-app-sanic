import os
import psycopg2
from asynctest import TestCase
from aiopg.sa import create_engine

from service_api.constants import BASIC_DB_CONFIG, DB_CONFIG

class InitDB:

    @staticmethod
    async def create_test_db():
        # Creating test database
        # print('Creating db {}'.format(self.__name__))
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                await conn.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))
                await conn.execute("CREATE DATABASE {} WITH OWNER = admin ;".format('test_db'))
        # con = psycopg2.connect(**BASIC_DB_CONFIG)
        # con.autocommit = True
        # cur = con.cursor()
        # cur.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))
        # cur.execute("CREATE DATABASE {} WITH OWNER = admin ;".format('test_db'))
        # cur.close()

        # Automatic migration
        script_dir = os.path.dirname(__file__)
        LIQUIBASE_COMMAND = """
                        sudo {} --driver={} --classpath={} --changeLogFile={} --url={} --username={} --password={} --logLevel=info {}
                    """
        liquibase_command = LIQUIBASE_COMMAND.format(
            os.path.join(script_dir, "../../migrations/liquibase"),
            "org.postgresql.Driver",
            os.path.join(script_dir, "../../migrations/jdbcdrivers/postgresql-42.2.5.jar"),
            os.path.join(script_dir, "../../migrations/changelog.xml"),
            "jdbc:postgresql://localhost/test_db",
            'postgres',
            'admin',
            "migrate"
        )
        os.system(liquibase_command)

    @staticmethod
    async def remove_test_db():
        # print('Removing db {}'.format(self.__name__))
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                await conn.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))

        # con = psycopg2.connect(**BASIC_DB_CONFIG)
        # con.autocommit = True
        # cur = con.cursor()
        # cur.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))
        # cur.close()


class BaseTestCase(TestCase):

    @classmethod
    async def setUpClass(cls):
        await InitDB.create_test_db()

    @classmethod
    async def tearDownClass(cls):
        await InitDB.remove_test_db()

    async def test_get_all_tables(self):
        print('running base test')
        table_list = ('supply', 'clients', 'parseltype', 'parsel', 'storage')
        async with create_engine(**DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                result = [list(dict(r).values())[0]
                          async for r in conn.execute("SELECT table_name FROM information_schema.tables \
                                                              WHERE table_schema='public' ;")]
        self.assertEqual(len(result), 7)
        self.assertEqual(sorted(table_list), sorted(result[2:]))
