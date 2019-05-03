import os
import psycopg2
from aiopg.sa import create_engine
from asynctest import TestCase

from service_api.constants import TEST_DB_CONFIG, BASIC_DB_CONFIG
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.clients import (get_all_clients,
                                        insert_one_client,
                                        delete_all_clients,
                                        get_client_by_id,
                                        delete_one_client,
                                        update_client_by_id)


class ClientDomainTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Some pre-setup data
        cls.test_client = {
            "id": "31732169-9b7b-4f09-aa1b-7fecb350ab14",
            "name": "John",
            "email": "johnlara@mail.com",
            "age": 18,
            "address": "3073 Derek Drive"
        }
        cls.new_client = {
            "id": "31732169-9b7b-4f09-aa1b-7fecb350ab14",
            "name": "John Galt",
            "email": "johngalt@mail.com",
            "age": 38,
            "address": "3073 Derek Drive avenue"
        }
        cls.good_id = '31732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.bad_id = '49732169'
        cls.id_not_exist = '42732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.data = JsonLoader(get_abs_path('clients.json'))

        # Creating test database
        con = psycopg2.connect(**BASIC_DB_CONFIG)
        con.autocommit = True
        cur = con.cursor()
        cur.execute("DROP DATABASE IF EXISTS {}  ;".format('test_db'))
        cur.execute("CREATE DATABASE {}  ;".format('test_db'))
        cur.close()

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

    async def test_get_all_tables(self):
        table_list = ('supply', 'clients', 'parseltype', 'parsel', 'storage')
        async with create_engine(**TEST_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                result = [list(dict(r).values())[0]
                          async for r in conn.execute("SELECT table_name FROM information_schema.tables \
                                                              WHERE table_schema='public' ;")]
        self.assertEqual(len(result), 7)
        self.assertEqual(sorted(table_list), sorted(result[2:]))

    async def test_get_all_clients(self):
        for row in self.data.loaded_json:
            await insert_one_client(row, TEST_DB_CONFIG)
        test_result = await get_all_clients(TEST_DB_CONFIG)
        for row in test_result:
            row['id'] = str(row['id'])
        self.assertEqual(len(test_result), 4)
        self.assertEqual(test_result, list(self.data.loaded_json))
        await delete_all_clients(TEST_DB_CONFIG)

    async def test_get_client_by_id_exists(self):
        await insert_one_client(next(self.data.loaded_json), TEST_DB_CONFIG)
        test_result = await get_client_by_id(self.good_id, TEST_DB_CONFIG)
        test_result['id'] = str(test_result['id'])
        self.assertEqual(test_result, self.test_client)
        await delete_one_client(self.good_id, TEST_DB_CONFIG)

    async def test_get_client_by_id_not_exists(self):
        test_result = await get_client_by_id(self.id_not_exist, TEST_DB_CONFIG)
        self.assertEqual(test_result, [])

    async def test_get_client_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_client_by_id(self.bad_id, TEST_DB_CONFIG)

    async def test_insert_one_client(self):
        await insert_one_client(next(self.data.loaded_json), TEST_DB_CONFIG)
        async with create_engine(**TEST_DB_CONFIG) as engine:
            async with engine.acquire() as conn:
                result = [dict(r) async for r in conn.execute("SELECT * FROM clients;")]
        self.assertEqual(len(result), 1)
        await delete_one_client(self.good_id, TEST_DB_CONFIG)

    async def test_delete_all_clients(self):
        for row in self.data.loaded_json:
            await insert_one_client(row, TEST_DB_CONFIG)
        await delete_all_clients(TEST_DB_CONFIG)
        result = await get_all_clients(TEST_DB_CONFIG)
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    async def test_delete_one_client_exist(self):
        await insert_one_client(next(self.data.loaded_json), TEST_DB_CONFIG)
        result = await delete_one_client(self.good_id, TEST_DB_CONFIG)
        self.assertEqual(result['email'], "johnlara@mail.com")
        result = await get_all_clients(TEST_DB_CONFIG)
        self.assertEqual(len(result), 0)

    async def test_delete_one_client_not_exist(self):
        result = await delete_one_client(self.good_id, TEST_DB_CONFIG)
        self.assertEqual(result, [])

    async def test_update_client_by_id_exist(self):
        await insert_one_client(next(self.data.loaded_json), TEST_DB_CONFIG)
        result = await update_client_by_id(self.new_client, TEST_DB_CONFIG)
        self.assertEqual(result['email'], "johngalt@mail.com")
        result = await get_all_clients(TEST_DB_CONFIG)
        result['id'] = str(result['id'])
        self.assertEqual(result, self.new_client)

    @classmethod
    def tearDownClass(cls):
        con = psycopg2.connect(**BASIC_DB_CONFIG)
        con.autocommit = True
        cur = con.cursor()
        cur.execute("DROP DATABASE IF EXISTS {}  ;".format('test_db'))
        cur.close()
