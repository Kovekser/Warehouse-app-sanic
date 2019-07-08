import json
from asynctest import CoroutineMock, patch
from uuid import UUID
import datetime

from tests import BaseTestCase


class SupplyResourceTestCaseCase(BaseTestCase):
    with open('./tests/fixtures/supply.json') as f:
        select_all_data = json.load(f)
    one_supply = [{
        "id": UUID("3ac93c38-7114-43dd-810a-a11384be3fd8"),
        "from_storage": UUID("28a8e222-bd32-489a-b5ef-4370b9032c45"),
        "to_storage": UUID("5782c996-d0d0-4e4f-895e-e4a98f26c65f"),
        "status": "recieved",
        "client_id": UUID("357642d9-4ac0-47f2-a802-252d82fff10b"),
        "send_date": datetime.datetime(2019, 4, 9, 7, 10, 55, 859486),
        "received_date": datetime.datetime(2019, 4, 16, 7, 10, 55, 85952)
    }]

    @classmethod
    def setUpClass(cls):
        cls.url = f'{cls.base_url}/supply/3ac93c38-7114-43dd-810a-a11384be3fd8'
        cls.bold_url = f'{cls.base_url}/supply'
        cls.bad_url = f'{cls.base_url}/supply/123'
        cls.id_not_exist_url = f'{cls.base_url}/supply/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8'

    @patch('service_api.resources.supply_resource.get_all_supply',
           new=CoroutineMock(return_value=[]))
    def test_get_all_supply_resource_empty_table(self):
        request, response = self.test_client.get(self.bold_url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Supply": []})

    @patch('service_api.resources.supply_resource.get_all_supply',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_supply_resource_not_empty(self):

        row_keys = ("id", "from_storage", "to_storage", "status", "client_id", "send_date", "received_date")
        request, response = self.test_client.get(self.bold_url)

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Supply'], list)
        self.assertEqual(len(*response.json.values()), 9)

        for row in response.json['Supply']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.supply_resource.insert_one_supply',
           new=CoroutineMock())
    def test_post_one_supply_resource_valid(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "id": "3ac93c38-7114-43dd-810a-a11384be3fd8",
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "received",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": "2019-04-10",
                "received_date": "2019-04-20"
            })

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created supply'})

    def test_post_one_supply_resource_bad_types(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "id": "",
                "from_storage": "",
                "to_storage": "",
                "status": 123,
                "client_id": "",
                "send_date": "",
                "received_date": ""
            }
        )
        msg = {
            'Errors': {
                'client_id': ['Not a valid UUID.'],
                'from_storage': ['Not a valid UUID.'],
                'id': ['Not a valid UUID.'],
                'received_date': ['Not a valid datetime.'],
                'send_date': ['Not a valid datetime.'],
                'status': ['Not a valid string.'],
                'to_storage': ['Not a valid UUID.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_post_one_supply_resource_no_required(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={}
        )
        msg = {
            'Errors': {
                'client_id': ['Missing data for required field.'],
                'from_storage': ['Missing data for required field.'],
                'id': ['Missing data for required field.'],
                'send_date': ['Missing data for required field.'],
                'to_storage': ['Missing data for required field.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_post_one_supply_resource_bad_received_date(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "id": "3ac93c38-7114-43dd-810a-a11384be3fd8",
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "received",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": "2019-04-20",
                "received_date": "2019-04-10"
            }
        )
        msg = {'Errors': {'_schema': ["Receive date can't be earlier than send date!"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.delete_one_supply',
           new=CoroutineMock(return_value=[{'id': '3ac93c38-7114-43dd-810a-a11384be3fd8'}]))
    def test_delete_one_supply_resource_valid(self):
        request, response = self.test_client.delete(self.url)
        msg = {'msg': 'Successfully deleted supply 3ac93c38-7114-43dd-810a-a11384be3fd8'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    def test_delete_one_supply_resource_bad_id(self):
        request, response = self.test_client.delete(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.delete_one_supply',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_supply_resource_id_not_exist(self):
        request, response = self.test_client.delete(self.id_not_exist_url)
        msg = {'msg': 'Supply with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.update_supply_by_id',
           new=CoroutineMock(return_value=[{'id': '3ac93c38-7114-43dd-810a-a11384be3fd8'}]))
    def test_put_supply_resource_valid(self):
        request, response = self.test_client.put(
            self.url,
            json={
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "delivered",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": "2019-04-10",
                "received_date": "2019-04-20"
            }
        )
        msg = {'msg': 'Supply 3ac93c38-7114-43dd-810a-a11384be3fd8 successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    def test_put_supply_resource_bad_types(self):
        request, response = self.test_client.put(
            self.bad_url,
            json={
                "from_storage": "",
                "to_storage": "",
                "status": 123,
                "client_id": "",
                "send_date": "",
                "received_date": ""
            }
        )
        msg = {
            'Errors': {
                'client_id': ['Not a valid UUID.'],
                'from_storage': ['Not a valid UUID.'],
                'id': ['Not a valid UUID.'],
                'received_date': ['Not a valid datetime.'],
                'send_date': ['Not a valid datetime.'],
                'status': ['Not a valid string.'],
                'to_storage': ['Not a valid UUID.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_supply_resource_no_required(self):
        request, response = self.test_client.put(self.url, json={})
        msg = {
            'Errors': {
                'client_id': ['Missing data for required field.'],
                'from_storage': ['Missing data for required field.'],
                'send_date': ['Missing data for required field.'],
                'to_storage': ['Missing data for required field.']
            }
        }

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.update_supply_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_supply_resource_id_not_exist(self):
        request, response = self.test_client.put(
            self.id_not_exist_url,
            json={
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "delivered",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": "2019-04-10",
                "received_date": "2019-04-20"
            }
        )
        msg = {'msg': 'Supply with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_supply_resource_bad_receive_date(self):
        request, response = self.test_client.put(
            self.url,
            json={
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "delivered",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": "2019-04-20",
                "received_date": "2019-04-10"
            }
        )
        msg = {'Errors': {'_schema': ["Receive date can't be earlier than send date!"]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.get_supply_by_id',
           new=CoroutineMock(return_value=one_supply))
    def test_get_supply_by_id_exists_resource(self):
        request, response = self.test_client.get(self.url)
        supply_by_id = {
            "Supply": [{
                "id": "3ac93c38-7114-43dd-810a-a11384be3fd8",
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "recieved",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": 1554793855,
                "received_date": 1555398655
            }]
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, supply_by_id)

    @patch('service_api.resources.supply_resource.get_supply_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_supply_by_id_not_exists_resource(self):
        request, response = self.test_client.get(self.id_not_exist_url)
        msg = {'msg': 'Supply with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_get_supply_by_id_resource_bad_id(self):
        request, response = self.test_client.get(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)
