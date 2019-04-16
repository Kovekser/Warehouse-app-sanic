import json
from asynctest import TestCase, CoroutineMock, patch

from service_api.application import app


class SupplyResourceTestCase(TestCase):
    with open('./tests/fixtures/supply.json') as f:
        select_all_data = json.load(f)
    one_supply = {
        "id": "3ac93c38-7114-43dd-810a-a11384be3fd8",
        "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
        "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
        "status": "recieved",
        "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
        "send_date": 1554793855,
        "received_date": 1555398655
    }

    @classmethod
    def setUpClass(cls):
        cls.url = '/supply/3ac93c38-7114-43dd-810a-a11384be3fd8'

    @patch('service_api.resources.supply_resource.get_all_supply',
           new=CoroutineMock(return_value=[]))
    def test_get_all_supply_resource_empty_table(self):
        request, response = app.test_client.get('/supply')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Supply": []})

    @patch('service_api.resources.supply_resource.get_all_supply',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_supply_resource_not_empty(self):

        row_keys = ("id", "from_storage", "to_storage", "status", "client_id", "send_date", "received_date")
        request, response = app.test_client.get('/supply')

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Supply'], list)
        self.assertEqual(len(*response.json.values()), 7)

        for row in response.json['Supply']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.supply_resource.insert_one_supply',
           new=CoroutineMock(return_value=[]))
    def test_post_one_supply_resource(self):
        request, response = app.test_client.post('/supply')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created supply'})

    @patch('service_api.resources.supply_resource.delete_one_supply',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_supply_resource(self):
        request, response = app.test_client.delete(self.url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully deleted supply'})

    @patch('service_api.resources.supply_resource.update_supply_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_supply_resource(self):
        request, response = app.test_client.put(self.url)
        msg = {'msg': 'Supply 3ac93c38-7114-43dd-810a-a11384be3fd8 successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.supply_resource.get_supply_by_id',
           new=CoroutineMock(return_value=one_supply))
    def test_get_supply_by_id_exists_resource(self):
        request, response = app.test_client.get(self.url)
        supply_by_id = {
            "Supply": {
                "id": "3ac93c38-7114-43dd-810a-a11384be3fd8",
                "from_storage": "28a8e222-bd32-489a-b5ef-4370b9032c45",
                "to_storage": "5782c996-d0d0-4e4f-895e-e4a98f26c65f",
                "status": "recieved",
                "client_id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "send_date": 1554793855,
                "received_date": 1555398655
            }
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, supply_by_id)

    @patch('service_api.resources.supply_resource.get_supply_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_supply_by_id_not_exists_resource(self):
        request, response = app.test_client.get('/supply/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        msg = {'msg': 'Supply with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)
