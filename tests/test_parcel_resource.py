import json
from asynctest import TestCase, CoroutineMock, patch

from service_api.application import app


class ParcelResourceTestCase(TestCase):
    with open('./tests/fixtures/parcel.json') as f:
        select_all_data = json.load(f)
    one_parcel = {
        "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
        "description": "Food",
        "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
        "weight": 61,
        "cost": 16243,
        "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
    }

    @classmethod
    def setUpClass(cls):
        cls.url = '/parcel/d384a7d2-58a5-47f6-9f23-92b8d0d4dae8'
        cls.bold_url = '/parcel'
        cls.bad_url = '/parcel/123'
        cls.id_not_exist_url = '/parcel/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8'

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=[]))
    def test_get_all_parcel_resource_empty_table(self):
        request, response = app.test_client.get(self.bold_url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Parcels": []})

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_parcels_resource_not_empty(self):
        row_keys = ("id", "description", "type_id", "weight", "cost", "supply_id")
        request, response = app.test_client.get(self.bold_url)

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Parcels'], list)
        self.assertEqual(len(*response.json.values()), 6)

        for row in response.json['Parcels']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_resource_valid(self):
        request, response = app.test_client.post(self.bold_url, json={
            "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 61,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        })

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created parcel'})

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_resource_bad_types(self):
        request, response = app.test_client.post(self.bold_url, json={
            "id": "123",
            "description": 1111,
            "type_id": "",
            "weight": "",
            "cost": "",
            "supply_id": ""
        })
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

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_resource_no_required(self):
        request, response = app.test_client.post(self.bold_url, json={})
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

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_resource_bad_weight(self):
        request, response = app.test_client.post(self.bold_url, json={
            "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 2000,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        })
        msg = {'Errors': {'_schema': ["Parcel weight can't be greater than 1000"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value={'id': 'd384a7d2-58a5-47f6-9f23-92b8d0d4dae8'}))
    def test_delete_one_parcel_resource_valid(self):
        request, response = app.test_client.delete(self.url)

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully deleted parcel d384a7d2-58a5-47f6-9f23-92b8d0d4dae8'})

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_parcel_resource_bad_id(self):
        request, response = app.test_client.delete(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_parcel_resource_id_not_exist(self):
        request, response = app.test_client.delete(self.id_not_exist_url)
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value={'id': 'd384a7d2-58a5-47f6-9f23-92b8d0d4dae8'}))
    def test_put_parcel_resource_valid(self):
        request, response = app.test_client.put(self.url, json={
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 100,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        })
        msg = {'msg': 'Parcel d384a7d2-58a5-47f6-9f23-92b8d0d4dae8 successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_resource_bad_weight(self):
        request, response = app.test_client.put(self.url, json={
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 2000,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        })
        msg = {'Errors': {'_schema': ["Parcel weight can't be greater than 1000"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_resource_id_not_exist(self):
        request, response = app.test_client.put(self.id_not_exist_url, json={
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 200,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        })
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_resource_bad_types(self):
        request, response = app.test_client.put(self.bad_url, json={
            "description": 123,
            "type_id": "",
            "weight": "",
            "cost": "",
            "supply_id": ""
        })
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

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_resource_no_required(self):
        request, response = app.test_client.put(self.url, json={})
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
           new=CoroutineMock(return_value=one_parcel))
    def test_get_parcel_by_id_resource_valid(self):
        request, response = app.test_client.get(self.url)
        parcel_by_id = {
            "Parcel": {
                "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
                "description": "Food",
                "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
                "weight": 61,
                "cost": 16243,
                "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
            }
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, parcel_by_id)

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_by_id_not_exists_resource(self):
        request, response = app.test_client.get(self.id_not_exist_url)
        msg = {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_by_id_resource_bad_id(self):
        request, response = app.test_client.get(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)
