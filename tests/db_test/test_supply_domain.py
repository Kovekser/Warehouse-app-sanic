import psycopg2
import asyncio
import uuid
from copy import deepcopy
from dateutil.parser import parse

from tests.db_test import BaseDomainTest
from service_api.utils.load_json_data import get_dict_gen, load_json_data
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.supply import (get_all_supply,
                                       insert_one_supply,
                                       delete_all_supply,
                                       get_supply_by_id,
                                       delete_one_supply,
                                       update_supply_by_id)


class SupplyDomainTestCase(BaseDomainTest):
    @classmethod
    def setUpClass(cls):
        super(SupplyDomainTestCase, cls).setUpClass()

        cls.test_supply = [{
            "id": "04691388-56c1-4a49-8ae1-316c9439b026",
            "from_storage": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
            "to_storage": "6ca6522b-6a3d-48c4-8902-b1b28896aefe",
            "status": "awaiting",
            "client_id": "66962950-3c5a-488b-aae8-3eafff97575f",
            "send_date": "2019-04-09 07:10:55.859486",
            "received_date": "2019-04-16 07:10:55.85952"
        }]
        cls.new_supply = {
            "id": "04691388-56c1-4a49-8ae1-316c9439b026",
            "from_storage": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
            "to_storage": "6ca6522b-6a3d-48c4-8902-b1b28896aefe",
            "status": "delivered",
            "client_id": "66962950-3c5a-488b-aae8-3eafff97575f",
            "send_date": "2019-04-09 07:10:55.859486",
            "received_date": "2019-04-16 07:10:55.85952"
        }
        cls.good_id = '04691388-56c1-4a49-8ae1-316c9439b026'
        cls.bad_id = '49732169'
        cls.id_not_exist = '42732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.data = JsonLoader(get_abs_path('supply.json'))
        cls.types = [uuid.UUID, uuid.UUID, uuid.UUID, str, uuid.UUID, parse, parse]

        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(
            load_json_data(get_dict_gen([get_abs_path(f) for f in ['storage.json', 'clients.json']]))
        )

    async def setUp(self):
        await delete_all_supply()

    async def test_get_all_supply(self):
        for row in self.data.loaded_json:
            await insert_one_supply(row)
        test_result, _ = await get_all_supply()
        expected = list(self.data.loaded_json)
        for i, row in enumerate(expected):
            expected[i] = {d[0]: t(d[1]) for t, d in zip(self.types, row.items())}
        self.assertEqual(len(test_result), 9)
        self.assertEqual(test_result, expected)

    async def test_get_supply_by_id_exists(self):
        await insert_one_supply(next(self.data.loaded_json))
        test_result, _ = await get_supply_by_id(self.good_id)
        expected = deepcopy(self.test_supply)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected[0].items())}
        self.assertEqual(1, len(test_result))
        self.assertEqual(test_result[0], expected)

    async def test_get_supply_by_id_not_exists(self):
        test_result, _ = await get_supply_by_id(self.id_not_exist)
        self.assertEqual(test_result, [])

    async def test_get_supply_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_supply_by_id(self.bad_id)

    async def test_insert_one_supply(self):
        await insert_one_supply(next(self.data.loaded_json))
        result, _ = await get_all_supply()
        expected = deepcopy(self.test_supply)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected[0].items())}
        self.assertEqual(1, len(result))
        self.assertEqual(result[0], expected)

    async def test_delete_all_supply(self):
        for row in self.data.loaded_json:
            await insert_one_supply(row)
        result, _ = await get_all_supply()
        self.assertEqual(len(result), 9)
        await delete_all_supply()
        result, _ = await get_all_supply()
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    async def test_delete_one_supply_exist(self):
        await insert_one_supply(next(self.data.loaded_json))
        result, _ = await get_all_supply()
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)
        result, _ = await delete_one_supply(self.good_id)
        expected = uuid.UUID(self.good_id)
        self.assertEqual(result[0]['id'], expected)
        result, _ = await get_all_supply()
        self.assertEqual(len(result), 0)

    async def test_delete_one_supply_not_exist(self):
        result, _ = await delete_one_supply(self.id_not_exist)
        self.assertEqual(result, [])

    async def test_update_supply_by_id_exist(self):
        await insert_one_supply(next(self.data.loaded_json))
        updated_result, _ = await update_supply_by_id(self.new_supply)
        all_supply, _ = await get_all_supply()
        expected = deepcopy(self.new_supply)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected.items())}
        self.assertEqual(1, len(all_supply))
        self.assertEqual(updated_result[0]['id'], expected['id'])
        self.assertEqual(all_supply[0], expected)
