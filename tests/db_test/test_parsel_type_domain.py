import psycopg2
import uuid
from copy import deepcopy

from tests.db_test import BaseDomainTest
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.parsel_type import (get_all_types,
                                            insert_one_type,
                                            delete_all_type,
                                            get_type_by_id,
                                            delete_one_type,
                                            update_type_by_id
                                            )


class ParselTypeDomainTestCase(BaseDomainTest):
    @classmethod
    def setUpClass(cls):
        super(ParselTypeDomainTestCase, cls).setUpClass()

        cls.test_type = {
            "id": "78f6f9ca-2771-406e-a926-db8c5006c605",
            "type_name": "documents"
        }
        cls.new_type = {
            "id": "78f6f9ca-2771-406e-a926-db8c5006c605",
            "type_name": "very important documents"
        }
        cls.good_id = '78f6f9ca-2771-406e-a926-db8c5006c605'
        cls.bad_id = '49732169'
        cls.id_not_exist = '42732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.data = JsonLoader(get_abs_path('parceltype.json'))

    async def setUp(self):
        await delete_all_type()

    async def test_get_all_types(self):
        for row in self.data.loaded_json:
            await insert_one_type(row)
        test_result = await get_all_types()
        for row in test_result:
            row['id'] = str(row['id'])
        self.assertEqual(len(test_result), 5)
        self.assertEqual(test_result, list(self.data.loaded_json))

    async def test_get_type_by_id_exists(self):
        await insert_one_type(next(self.data.loaded_json))
        test_result = await get_type_by_id(self.good_id)
        expected = deepcopy(self.test_type)
        expected['id'] = uuid.UUID(expected['id'])
        self.assertIsInstance(test_result, list)
        self.assertEqual(1, len(test_result))
        self.assertEqual(test_result[0], expected)

    async def test_get_type_by_id_not_exists(self):
        test_result = await get_type_by_id(self.id_not_exist)
        self.assertEqual(test_result, [])

    async def test_get_type_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_type_by_id(self.bad_id)

    async def test_insert_one_type(self):
        await insert_one_type(next(self.data.loaded_json))
        result = await get_all_types()
        expected = deepcopy(self.test_type)
        expected['id'] = uuid.UUID(expected['id'])
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], expected)

    async def test_delete_all_types(self):
        for row in self.data.loaded_json:
            await insert_one_type(row)
        result = await get_all_types()
        self.assertEqual(len(result), 5)
        await delete_all_type()
        result = await get_all_types()
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    async def test_delete_one_type_exist(self):
        await insert_one_type(self.test_type)
        result = await get_all_types()
        self.assertIsInstance(result, list)
        self.assertEqual(1, len(result))
        result = await delete_one_type(self.good_id)
        self.assertEqual(result[0]['type_name'], 'documents')
        result = await get_all_types()
        self.assertEqual(len(result), 0)

    async def test_delete_one_type_not_exist(self):
        result = await delete_one_type(self.id_not_exist)
        self.assertEqual(result, [])

    async def test_update_type_by_id_exist(self):
        await insert_one_type(self.test_type)
        result = await update_type_by_id(self.new_type)
        self.assertEqual(result[0]['type_name'], 'very important documents')
        result = await get_all_types()
        expected = deepcopy(self.new_type)
        expected['id'] = uuid.UUID(expected['id'])
        self.assertEqual(result[0], expected)
