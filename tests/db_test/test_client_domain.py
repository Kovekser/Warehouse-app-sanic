import psycopg2

from tests.db_test import BaseTestCase
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.clients import (get_all_clients,
                                        insert_one_client,
                                        delete_all_clients,
                                        get_client_by_id,
                                        delete_one_client,
                                        update_client_by_id)


class ClientDomainTestCase(BaseTestCase):
    @classmethod
    async def setUpClass(cls):
        # Some pre-setup data
        BaseTestCase.setUpClass()

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

    async def test_get_all_clients(self):
        print('running client tests')
        for row in self.data.loaded_json:
            await insert_one_client(row)
        test_result = await get_all_clients()
        for row in test_result:
            row['id'] = str(row['id'])
        self.assertEqual(len(test_result), 4)
        self.assertEqual(test_result, list(self.data.loaded_json))
        await delete_all_clients()

    async def test_get_client_by_id_exists(self):
        await insert_one_client(next(self.data.loaded_json))
        test_result = await get_client_by_id(self.good_id)
        test_result['id'] = str(test_result['id'])
        self.assertEqual(test_result, self.test_client)
        await delete_one_client(self.good_id)

    async def test_get_client_by_id_not_exists(self):
        test_result = await get_client_by_id(self.id_not_exist)
        self.assertEqual(test_result, [])

    async def test_get_client_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_client_by_id(self.bad_id)

    async def test_insert_one_client(self):
        await insert_one_client(next(self.data.loaded_json))
        result = await get_all_clients()
        self.assertEqual(len(result), 1)
        await delete_one_client(self.good_id)

    async def test_delete_all_clients(self):
        for row in self.data.loaded_json:
            await insert_one_client(row)
        await delete_all_clients()
        result = await get_all_clients()
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    async def test_delete_one_client_exist(self):
        await insert_one_client(next(self.data.loaded_json))
        result = await delete_one_client(self.good_id)
        self.assertEqual(result['email'], "johnlara@mail.com")
        result = await get_all_clients()
        self.assertEqual(len(result), 0)

    async def test_delete_one_client_not_exist(self):
        result = await delete_one_client(self.id_not_exist)
        self.assertEqual(result, [])

    async def test_update_client_by_id_exist(self):
        await insert_one_client(next(self.data.loaded_json))
        result = await update_client_by_id(self.new_client)
        self.assertEqual(result['email'], "johngalt@mail.com")
        result = await get_all_clients()
        result['id'] = str(result['id'])
        self.assertEqual(result, self.new_client)
        await delete_all_clients()
