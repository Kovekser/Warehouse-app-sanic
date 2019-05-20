import psycopg2
import asyncio
import uuid
from copy import deepcopy
from decimal import Context

from tests.db_test.test_base import BaseTestCase
from service_api.utils.load_json_data import get_dict_gen, load_json_data
from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path
from service_api.domain.parcel import (get_all_parcels,
                                       insert_one_parcel,
                                       delete_all_parcel,
                                       get_parcel_by_id,
                                       delete_one_parcel,
                                       update_parcel_by_id)


class ParcelDomainTestCase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        super(ParcelDomainTestCase, cls).setUpClass()

        cls.test_parcel = {
            "id": "720745e2-cee6-4338-8399-72b6affb71a6",
            "description": "Food",
            "type_id": "ac13d5ee-61ba-4945-b5e8-a84d8da5a885",
            "weight": 17.3,
            "cost": 381.6,
            "supply_id": "7542e12a-c30b-4e68-9b22-42dbc477cb5a"
        }
        cls.new_parcel = {
            "id": "720745e2-cee6-4338-8399-72b6affb71a6",
            "description": "Food",
            "type_id": "ac13d5ee-61ba-4945-b5e8-a84d8da5a885",
            "weight": 20,
            "cost": 381.6,
            "supply_id": "dcf19a78-b01f-4251-924f-3403df3afdaf"
        }
        cls.good_id = '720745e2-cee6-4338-8399-72b6affb71a6'
        cls.bad_id = '49732169'
        cls.id_not_exist = '42732169-9b7b-4f09-aa1b-7fecb350ab14'
        cls.data = JsonLoader(get_abs_path('parcel.json'))

        cls.ctx = Context(prec=5)
        cls.types = [uuid.UUID, str, uuid.UUID, cls.ctx.create_decimal_from_float,
                     cls.ctx.create_decimal_from_float, uuid.UUID]

        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(
            load_json_data(get_dict_gen([get_abs_path(f)
                                         for f in
                                         ['parceltype.json', 'clients.json', 'storage.json', 'supply.json']]))
        )

    async def setUp(self):
        await delete_all_parcel()

    async def test_get_all_parcel(self):
        for row in self.data.loaded_json:
            await insert_one_parcel(row)
        test_result = await get_all_parcels()
        expected = list(self.data.loaded_json)
        for i, row in enumerate(expected):
            expected[i] = {d[0]: t(d[1]) for t, d in zip(self.types, row.items())}
        self.assertEqual(len(test_result), 6)
        self.assertEqual(test_result, expected)

    async def test_get_parcel_by_id_exists(self):
        await insert_one_parcel(next(self.data.loaded_json))
        test_result = await get_parcel_by_id(self.good_id)
        expected = deepcopy(self.test_parcel)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected.items())}
        self.assertEqual(test_result, expected)

    async def test_get_parcel_by_id_not_exists(self):
        test_result = await get_parcel_by_id(self.id_not_exist)
        self.assertEqual(test_result, [])

    async def test_get_parcel_by_id_bad(self):
        with self.assertRaises(psycopg2.DataError):
            await get_parcel_by_id(self.bad_id)

    async def test_insert_one_parcel(self):
        await insert_one_parcel(next(self.data.loaded_json))
        result = await get_all_parcels()
        expected = deepcopy(self.test_parcel)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected.items())}
        self.assertEqual(result, expected)

    async def test_delete_all_parcel(self):
        for row in self.data.loaded_json:
            await insert_one_parcel(row)
        result = await get_all_parcels()
        expected = list(self.data.loaded_json)
        for i, row in enumerate(expected):
            expected[i] = {d[0]: t(d[1]) for t, d in zip(self.types, row.items())}
        self.assertEqual(len(result), 6)
        await delete_all_parcel()
        result = await get_all_parcels()
        self.assertEqual(len(result), 0)
        self.assertEqual(result, [])

    async def test_delete_one_parcel_exist(self):
        await insert_one_parcel(next(self.data.loaded_json))
        result = await get_parcel_by_id(self.good_id)
        self.assertIsInstance(result, dict)
        result = await delete_one_parcel(self.good_id)
        expected = uuid.UUID(self.good_id)
        self.assertEqual(result['id'], expected)
        result = await get_all_parcels()
        self.assertEqual(len(result), 0)

    async def test_delete_one_parcel_not_exist(self):
        result = await delete_one_parcel(self.id_not_exist)
        self.assertEqual(result, [])

    async def test_update_parcel_by_id_exist(self):
        await insert_one_parcel(next(self.data.loaded_json))
        updated_result = await update_parcel_by_id(self.new_parcel)
        get_result = await get_all_parcels()
        expected = deepcopy(self.new_parcel)
        expected = {d[0]: t(d[1]) for t, d in zip(self.types, expected.items())}
        self.assertEqual(updated_result['id'], expected['id'])
        self.assertEqual(get_result, expected)