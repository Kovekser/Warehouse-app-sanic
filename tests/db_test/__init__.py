import os
import asyncio
from aiopg.sa import create_engine

from service_api.constants import BASIC_DB_CONFIG, DB_CONFIG

from tests import BaseTestCase


class InitDB:

    @staticmethod
    async def create_test_db():
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                await conn.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))
                await conn.execute("CREATE DATABASE {} WITH OWNER = admin ;".format('test_db'))

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
        async with create_engine(**BASIC_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                conn.autocommit = True
                await conn.execute("DROP DATABASE IF EXISTS {} ;".format('test_db'))


class BaseDomainTest(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(InitDB.create_test_db())

    @classmethod
    def tearDownClass(cls):
        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(InitDB.remove_test_db())

    async def test_get_all_tables(self):
        table_list = ('supply', 'clients', 'parseltype', 'parsel', 'storage')
        async with create_engine(**DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                result = [list(dict(r).values())[0]
                          async for r in conn.execute("SELECT table_name FROM information_schema.tables \
                                                                  WHERE table_schema='public' ;")]
        self.assertEqual(len(result), 7)
        self.assertEqual(sorted(table_list), sorted(result[2:]))
