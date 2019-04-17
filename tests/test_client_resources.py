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
    def test_post_one_client_resource_valid_data(self):
        request, response = app.test_client.post('/client', json={
            "id": "357642d9-4ac0-47f2-a802-252d82fff10b",
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created user'})

    @patch('service_api.resources.client_resource.insert_one_client',
           new=CoroutineMock(return_value=[]))
    def test_post_one_client_resource_no_id(self):
        request, response = app.test_client.post('/client', json={
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'id': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.insert_one_client',
           new=CoroutineMock(return_value=[]))
    def test_post_one_client_resource_bad_id(self):
        request, response = app.test_client.post('/client', json={
            "id": "12345",
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.insert_one_client',
           new=CoroutineMock(return_value=[]))
    def test_post_one_client_resource_bad_email(self):
        request, response = app.test_client.post('/client', json={
            "id": "357642d9-4ac0-47f2-a802-252d82fff10b",
            "address": "3494 gfhfghgfh",
            "email": "INVALID",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'email': ['Not a valid email address']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.insert_one_client',
           new=CoroutineMock(return_value=[]))
    def test_post_one_client_resource_bad_email_bad_id(self):
        request, response = app.test_client.post('/client', json={
            "id": "123",
            "address": "3494 gfhfghgfh",
            "email": "INVALID",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'email': ['Not a valid email address'],
                          'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.delete_one_client',
           new=CoroutineMock(return_value={'email': 'pablogibson@mail.com'}))
    def test_delete_one_client_resource_id_exist(self):
        request, response = app.test_client.delete(self.url)
        msg = {'msg': 'Successfully deleted user pablogibson@mail.com'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.delete_one_client',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_client_resource_bad_id(self):
        request, response = app.test_client.delete('/client/123')
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.delete_one_client',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_client_resource_id_not_exist(self):
        request, response = app.test_client.delete('/client/657642d9-4ac0-47f2-a802-252d82fff10b')
        msg = {'msg': 'User with id 657642d9-4ac0-47f2-a802-252d82fff10b does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.update_client_by_id',
           new=CoroutineMock(return_value={'email': 'pablo@gmail.com'}))
    def test_put_client_resource_id_exist_valid_data(self):
        request, response = app.test_client.put(self.url, json={
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        msg = {'msg': 'User pablo@gmail.com successfully updated'}

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, msg)

    def test_put_client_resource_bad_id(self):
        request, response = app.test_client.put('/client/3', json={
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_client_resource_id_not_exist(self):
        request, response = app.test_client.put('/client/457642d9-4ac0-47f2-a802-252d82fff10b', json={
            "address": "3494 gfhfghgfh",
            "email": "pablo@gmail.com",
            "name": "Pablo piCASso"
        })
        msg = {'msg': 'User with id 457642d9-4ac0-47f2-a802-252d82fff10b does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_client_resource_id_exist_bad_email(self):
        request, response = app.test_client.put(self.url, json={
            "address": "3494 gfhfghgfh",
            "email": "pablogmailcom",
            "name": "Pablo piCASso"
        })
        msg = {"Errors": {
            "email": ["Not a valid email address"]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    def test_put_client_resource_bad_id_bad_email(self):
        request, response = app.test_client.put('/client/123', json={
            "address": "3494 gfhfghgfh",
            "email": "pablogmailcom",
            "name": "Pablo piCASso"
        })
        msg = {'Errors': {'email': ['Not a valid email address'],
                          'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
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

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.client_resource.get_client_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_client_by_id_resource_bad_id(self):
        request, response = app.test_client.get('/client/123')
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)
