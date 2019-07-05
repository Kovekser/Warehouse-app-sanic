import psycopg2
import uuid
from copy import deepcopy

from tests.db_test import BaseDomainTest
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.storage import (get_all_storage,
                                        insert_one_storage,
                                        delete_all_storage,
                                        get_storage_by_id,
                                        delete_one_storage,
                                        update_storage_by_id)


class StorageDomainTestCase(BaseDomainTest):
    @classmethod
    def setUpClass(cls):
        super(StorageDomainTestCase, cls).setUpClass()

        cls.test_storage = {
            "id": "0148bc1a-90c7-451b-aecc-7081e0f4b60a",
            "address": "197D Klochkovska str.",
            "max_weight": 1000,
            "max_capacity": 30000
        }
        cls.new_storage = {
            "id": "0148bc1a-90c7-451b-aecc-7081e0f4b60a",
            "address": "222 Valentynivska str., apt. 39",
            "max_weight": 100,
            "max_capacity": 20000
        }
        cls.good_id = '0148bc1a-90c7-451b-aecc-7081e0f4b60a'
        cls.bad_id = '49732169'
        cls.id_not_exist = '42732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.data = JsonLoader(get_abs_path('storage.json'))

    async def setUp(self):
        await delete_all_storage()

    async def test_get_all_storage(self):
        for row in self.data.loaded_json:
            await insert_one_storage(row)
        test_result, _ = await get_all_storage()
        for row in test_result:
            row['id'] = str(row['id'])
        self.assertEqual(len(test_result), 7)
        self.assertEqual(test_result, list(self.data.loaded_json))

    async def test_get_storage_by_id_exists(self):
        await insert_one_storage(next(self.data.loaded_json))
        test_result, _ = await get_storage_by_id(self.good_id)
        expected = deepcopy(self.test_storage)
        expected['id'] = uuid.UUID(expected['id'])

        self.assertIsInstance(test_result, list)
        self.assertEqual(1, len(test_result))
        self.assertEqual(test_result[0], expected)

    async def test_get_storage_by_id_not_exists(self):
        test_result, _ = await get_storage_by_id(self.id_not_exist)
        self.assertEqual(test_result, [])

    async def test_get_storage_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_storage_by_id(self.bad_id)

    async def test_insert_one_storage(self):
        await insert_one_storage(next(self.data.loaded_json))
        result, _ = await get_all_storage()
        expected = deepcopy(self.test_storage)
        expected['id'] = uuid.UUID(expected['id'])

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], expected)

    async def test_delete_all_storage(self):
        for row in self.data.loaded_json:
            await insert_one_storage(row)
        result, _ = await get_all_storage()
        self.assertEqual(len(result), 7)
        await delete_all_storage()
        result, _ = await get_all_storage()
        self.assertEqual(result, [])

    async def test_delete_one_storage_exist(self):
        await insert_one_storage(next(self.data.loaded_json))
        result, _ = await get_all_storage()
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        result, _ = await delete_one_storage(self.good_id)
        self.assertEqual(result[0]['address'], '197D Klochkovska str.')
        result, _ = await get_all_storage()
        self.assertEqual(len(result), 0)

    async def test_delete_one_storage_not_exist(self):
        result, _ = await delete_one_storage(self.id_not_exist)
        self.assertEqual(result, [])

    async def test_update_storage_by_id_exist(self):
        await insert_one_storage(next(self.data.loaded_json))
        result, _ = await update_storage_by_id(self.new_storage)
        self.assertEqual(result[0]['address'], '222 Valentynivska str., apt. 39')
        result, _ = await get_all_storage()
        expected = deepcopy(self.new_storage)
        expected['id'] = uuid.UUID(expected['id'])

        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], expected)
