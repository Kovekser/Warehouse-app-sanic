import json
from asynctest import TestCase, CoroutineMock, patch

from service_api.application import app


class SmokeEndPointTestCase(TestCase):
    def test_smoke_end_point(self):
        request, response = app.test_client.get('/smoke')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'Result': 'This is a smoke view'})


class ClientResourceTestCase(TestCase):
    with open('./tests/fixtures/clients.json') as f:
        select_all_data = json.load(f)
    one_client = {
        "id": "357642d9-4ac0-47f2-a802-252d82fff10b",
        "name": "Pablo",
        "email": "pablogibson@mail.com",
        "age": 52,
        "address": "3494 Murry Street"
    }

    @classmethod
    def setUpClass(cls):
        cls.url = '/client/357642d9-4ac0-47f2-a802-252d82fff10b'

    @patch('service_api.resources.client_resource.get_all_clients',
           new=CoroutineMock(return_value=[]))
    def test_get_all_clients_resource_empty_table(self):
        request, response = app.test_client.get('/client')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Clients": []})

    @patch('service_api.resources.client_resource.get_all_clients',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_clients_resource_not_empty(self):
        row_keys = ("id", "name", "email", "age", "address")
        request, response = app.test_client.get('/client')

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Clients'], list)
        self.assertEqual(len(*response.json.values()), 4)

        for row in response.json['Clients']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.client_resource.insert_one_client',
           new=CoroutineMock(return_value=[]))
    def test_post_one_client_resource(self):
        request, response = app.test_client.post('/client')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created user'})

    @patch('service_api.resources.client_resource.get_client_by_id',
           new=CoroutineMock(return_value=one_client))
    @patch('service_api.resources.client_resource.delete_one_client',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_client_resource(self):
        request, response = app.test_client.delete(self.url)
        msg = {'msg': 'Successfully deleted user pablogibson@mail.com'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.get_client_by_id',
           new=CoroutineMock(return_value=one_client))
    @patch('service_api.resources.client_resource.update_client_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_client_resource(self):
        request, response = app.test_client.put(self.url)
        msg = {'msg': 'User pablogibson@mail.com successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.get_client_by_id',
           new=CoroutineMock(return_value=one_client))
    def test_get_client_by_id_exist_resource(self):
        request, response = app.test_client.get(self.url)
        client_by_id = {
            "Client": {
                "id": "357642d9-4ac0-47f2-a802-252d82fff10b",
                "name": "Pablo",
                "email": "pablogibson@mail.com",
                "age": 52,
                "address": "3494 Murry Street"
            }
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, client_by_id)

    @patch('service_api.resources.client_resource.get_client_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_client_by_id_not_exist_resource(self):
        request, response = app.test_client.get('/client/468642d9-4ac0-47f2-a802-252d82fff10b')
        msg = {'msg': 'Client with id 468642d9-4ac0-47f2-a802-252d82fff10b does not exist'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)
