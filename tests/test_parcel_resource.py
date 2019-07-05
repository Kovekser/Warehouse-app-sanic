import json
from asynctest import CoroutineMock, patch
from uuid import UUID
import datetime
import calendar
from decimal import Decimal
from copy import deepcopy

from tests import BaseTestCase


class ParcelResourceTestCaseCase(BaseTestCase):
    with open('./tests/fixtures/parcel.json') as f:
        select_all_data = json.load(f)
    one_parcel = [{
        "id": UUID("d384a7d2-58a5-47f6-9f23-92b8d0d4dae8"),
        "description": "Food",
        "type_id": UUID("d8134182-6cbf-4aba-9cbe-4a3396ad430c"),
        "weight": Decimal('61'),
        "cost": Decimal('16243'),
        "supply_id": UUID("3ac93c38-7114-43dd-810a-a11384be3fd8")
    }]

    @classmethod
    def setUpClass(cls):
        cls.url = '/parcel/d384a7d2-58a5-47f6-9f23-92b8d0d4dae8'
        cls.bad_url = '/parcel/123'
        cls.id_not_exist_url = '/parcel/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8'

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=([], '')))
    def test_get_all_parcel_resource_empty_table(self):
        request, response = self.test_client.get(f'{self.base_url}/parcel')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Parcels": []})

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=(select_all_data, '')))
    def test_get_all_parcels_resource_not_empty(self):
        row_keys = ("id", "description", "type_id", "weight", "cost", "supply_id")
        request, response = self.test_client.get(f'{self.base_url}/parcel')

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Parcels'], list)
        self.assertEqual(len(*response.json.values()), 7)

        for row in response.json['Parcels']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock())
    def test_post_one_parcel_resource_valid(self):
        request, response = self.test_client.post(
            f'{self.base_url}/parcel',
            json={
                "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 61,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        )

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created parcel'})

    def test_post_one_parcel_resource_bad_types(self):
        request, response = self.test_client.post(
            f'{self.base_url}/parcel',
            json={
                "id": "123",
                "description": 1111,
                "type_id": "",
                "weight": "",
                "cost": "",
                "supply_id": ""
            }
        )
        msg = {
            'Errors': {
                'cost': ['Not a valid number.'],
                'description': ['Not a valid string.'],
                'id': ['Not a valid UUID.'],
                'supply_id': ['Not a valid UUID.'],
                'type_id': ['Not a valid UUID.'],
                'weight': ['Not a valid number.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_post_one_parcel_resource_no_required_data(self):
        request, response = self.test_client.post(f'{self.base_url}/parcel', json={})
        msg = {
            'Errors': {
                'cost': ['Missing data for required field.'],
                'id': ['Missing data for required field.'],
                'supply_id': ['Missing data for required field.'],
                'type_id': ['Missing data for required field.'],
                'weight': ['Missing data for required field.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_post_one_parcel_resource_bad_weight(self):
        request, response = self.test_client.post(
            f'{self.base_url}/parcel',
            json={
                "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 2000,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        )
        msg = {'Errors': {'_schema': ["Parcel weight can't be greater than 1000"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value=([{'id': 'd384a7d2-58a5-47f6-9f23-92b8d0d4dae8'}], '')))
    def test_delete_one_parcel_resource_valid(self):
        request, response = self.test_client.delete(f'{self.base_url}{self.url}')

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully deleted parcel d384a7d2-58a5-47f6-9f23-92b8d0d4dae8'})

    def test_delete_one_parcel_resource_bad_id(self):
        request, response = self.test_client.delete(f'{self.base_url}{self.bad_url}')
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value=([], '')))
    def test_delete_one_parcel_resource_id_not_exist(self):
        request, response = self.test_client.delete(f'{self.base_url}{self.id_not_exist_url}')
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=([{'id': 'd384a7d2-58a5-47f6-9f23-92b8d0d4dae8'}],'')))
    def test_put_parcel_resource_valid(self):
        request, response = self.test_client.put(
            f'{self.base_url}{self.url}',
            json={
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 100,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        )
        msg = {'msg': 'Parcel d384a7d2-58a5-47f6-9f23-92b8d0d4dae8 successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    def test_put_parcel_resource_bad_weight(self):
        request, response = self.test_client.put(
            f'{self.base_url}{self.url}',
            json={
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 2000,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        )
        msg = {'Errors': {'_schema': ["Parcel weight can't be greater than 1000"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=([], '')))
    def test_put_parcel_resource_id_not_exist(self):
        request, response = self.test_client.put(
            f'{self.base_url}{self.id_not_exist_url}',
            json={
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 200,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        )
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_parcel_resource_bad_types(self):
        request, response = self.test_client.put(
            f'{self.base_url}{self.bad_url}',
            json={
                "description": 123,
                "type_id": "",
                "weight": "",
                "cost": "",
                "supply_id": ""
            }
        )
        msg = {
            'Errors': {
                'cost': ['Not a valid number.'],
                'description': ['Not a valid string.'],
                'id': ['Not a valid UUID.'],
                'supply_id': ['Not a valid UUID.'],
                'type_id': ['Not a valid UUID.'],
                'weight': ['Not a valid number.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_parcel_resource_no_required(self):
        request, response = self.test_client.put(f'{self.base_url}{self.url}', json={})
        msg = {
            'Errors': {
                'cost': ['Missing data for required field.'],
                'supply_id': ['Missing data for required field.'],
                'type_id': ['Missing data for required field.'],
                'weight': ['Missing data for required field.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=(one_parcel, '')))
    def test_get_parcel_by_id_resource_valid(self):
        request, response = self.test_client.get(f'{self.base_url}{self.url}')
        parcel_by_id = {
            "Parcel": [{
                "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 61,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }]
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, parcel_by_id)

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=([], '')))
    def test_get_parcel_by_id_not_exists_resource(self):
        request, response = self.test_client.get(f'{self.base_url}{self.id_not_exist_url}')
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_get_parcel_by_id_resource_bad_id(self):
        request, response = self.test_client.get(f'{self.base_url}{self.bad_url}')
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)


class ParcelQueryResourceTestCase(BaseTestCase):
    valid_response_one_row = [{'parcel_id': UUID('36461812-998b-40f4-98a1-35cbe7919d43'),
                              'description': 'Food', 'cost': Decimal('16243'),
                              'type_name': 'medium_box', 'client_name': 'Derek',
                              'address': '76 Matiushenko str.',
                              'received_date': datetime.datetime(2019, 4, 16, 7, 10, 55, 859520)}]
    valid_response_two_rows = [{'parcel_id': UUID('36461812-998b-40f4-98a1-35cbe7919d43'),
                                'description': 'Food', 'cost': Decimal('16243'),
                                'type_name': 'medium_box', 'client_name': 'Derek',
                                'address': '76 Matiushenko str.',
                                'received_date': datetime.datetime(2019, 4, 16, 7, 10, 55, 859520)},
                               {'parcel_id': UUID('67ea2c74-2831-40f2-8109-eadb8dcdcd58'),
                                'description': 'Other goods', 'cost': Decimal('7891'),
                                'type_name': 'medium_box', 'client_name': 'Derek',
                                'address': '76 Matiushenko str.',
                                'received_date': datetime.datetime(2019, 4, 18, 7, 10, 55, 859520)}]

    @classmethod
    def setUpClass(cls):
        cls.valid_url_no_date = f'{cls.base_url}/parcel/medium_box/5782c996-d0d0-4e4f-895e-e4a98f26c65f'
        cls.valid_url_one_date = f'{cls.base_url}/parcel/medium_box/5782c996-d0d0-4e4f-895e-e4a98f26c65f' \
                                 '?date=2019-04-16+07:10:55.85952'
        cls.valid_url_date_range = f'{cls.base_url}/parcel/medium_box/5782c996-d0d0-4e4f-895e-e4a98f26c65f' \
                                   '?date=2019-04-22&date=2019-04-10'
        cls.bad_id_url = f'{cls.base_url}/parcel/medium_box/123'
        cls.id_not_exist_url = f'{cls.base_url}/parcel/medium_box/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8'

    def test_get_parcel_by_type_and_storage_bad_id(self):
        request, response = self.test_client.get(self.bad_id_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.get_parcel_by_type_and_storage',
           new=CoroutineMock(return_value=(valid_response_two_rows, '')))
    def test_get_parcel_by_type_and_storage_no_date(self):
        request, response = self.test_client.get(self.valid_url_no_date)
        expected = deepcopy(self.valid_response_two_rows)
        for row in expected:
            row['parcel_id'] = str(row['parcel_id'])
            row['cost'] = float(row['cost'])
            row['received_date'] = calendar.timegm(row['received_date'].timetuple())

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('parcels', response.json)
        self.assertIn('total_cost', response.json)
        self.assertIsInstance(response.json['parcels'], list)
        self.assertEqual(response.json['total_cost'], Decimal('24134'))
        self.assertEqual(response.json['parcels'], expected)

    @patch('service_api.resources.parcel_resource.get_parcel_by_type_and_storage',
           new=CoroutineMock(return_value=(valid_response_two_rows, '')))
    def test_get_parcel_by_type_and_storage_date_range(self):
        request, response = self.test_client.get(self.valid_url_date_range)
        self.assertEqual(request.args['date'], ['2019-04-22', '2019-04-10'])

        expected = deepcopy(self.valid_response_two_rows)
        for row in expected:
            row['parcel_id'] = str(row['parcel_id'])
            row['cost'] = float(row['cost'])
            row['received_date'] = calendar.timegm(row['received_date'].timetuple())

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('parcels', response.json)
        self.assertIn('total_cost', response.json)
        self.assertIsInstance(response.json['parcels'], list)
        self.assertEqual(response.json['total_cost'], Decimal('24134'))
        self.assertEqual(response.json['parcels'], expected)

    @patch('service_api.resources.parcel_resource.get_parcel_by_type_and_storage',
           new=CoroutineMock(return_value=(valid_response_one_row, '')))
    def test_get_parcel_by_type_and_storage_date_one(self):
        request, response = self.test_client.get(self.valid_url_one_date)
        self.assertEqual(request.args['date'], ['2019-04-16 07:10:55.85952'])

        expected = deepcopy(self.valid_response_one_row)
        expected[0]['parcel_id'] = str(expected[0]['parcel_id'])
        expected[0]['cost'] = float(expected[0]['cost'])
        expected[0]['received_date'] = calendar.timegm(expected[0]['received_date'].timetuple())

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('parcels', response.json)
        self.assertIn('total_cost', response.json)
        self.assertIsInstance(response.json['parcels'], list)
        self.assertEqual(response.json['total_cost'], Decimal('16243'))
        self.assertEqual(response.json['parcels'], expected)

    @patch('service_api.resources.parcel_resource.get_parcel_by_type_and_storage',
           new=CoroutineMock(return_value=([], '')))
    def test_get_parcel_by_type_and_storage_empty_output(self):
        request, response = self.test_client.get(self.id_not_exist_url)

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIn('parcels', response.json)
        self.assertIn('total_cost', response.json)
        self.assertEqual(response.json['total_cost'], 0)
        self.assertEqual(response.json['parcels'], [])
