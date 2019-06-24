import json
from asynctest import CoroutineMock, patch
from uuid import UUID
from decimal import Decimal

from tests import BaseTestCase


class StorageResourceTestCaseCase(BaseTestCase):
    with open('./tests/fixtures/storage.json') as f:
        select_all_data = json.load(f)
    one_storage = {
        "id": UUID("fc6efd2d-86cb-4932-9acb-1ce97f8bb468"),
        "address": "197D Klochkovska str.",
        "max_weight": Decimal('1000'),
        "max_capacity": Decimal('30000')
    }

    @classmethod
    def setUpClass(cls):
        cls.url = '/storage/fc6efd2d-86cb-4932-9acb-1ce97f8bb468'
        cls.bold_url = '/storage'
        cls.bad_url = '/storage/123'
        cls.id_not_exist_url = '/storage/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8'

    @patch('service_api.resources.storage_resource.get_all_storage',
           new=CoroutineMock(return_value=[]))
    def test_get_all_storage_resource_empty_table(self):
        request, response = self.test_client.get(self.bold_url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {"Storages": []})

    @patch('service_api.resources.storage_resource.get_all_storage',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_storages_resource_not_empty(self):
        row_keys = ("id", "address", "max_weight", "max_capacity")
        request, response = self.test_client.get(self.bold_url)

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Storages'], list)
        self.assertEqual(len(*response.json.values()), 7)

        for row in response.json['Storages']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.storage_resource.insert_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_post_one_storage_resource_valid_data(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "id": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
                "address": "197D Klochkovska str.",
                "max_weight": 1000,
                "max_capacity": 30000
            }
        )

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created storage'})

    @patch('service_api.resources.storage_resource.insert_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_post_one_storage_resource_no_id(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "address": "197D Klochkovska str.",
                "max_weight": 1000,
                "max_capacity": 30000
            }
        )
        msg = {'Errors': {'id': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.insert_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_post_one_storage_resource_bad_types(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "id": "123",
                "address": 123,
                "max_weight": 'INVALID',
                "max_capacity": 'INVALID'
            }
        )
        msg = {'Errors': {'id': ['Not a valid UUID.'],
                          'max_capacity': ['Not a valid integer.'],
                          'max_weight': ['Not a valid integer.'],
                          'address': ['Not a valid string.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.insert_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_post_one_storage_resource_bad_types_no_id(self):
        request, response = self.test_client.post(
            self.bold_url,
            json={
                "address": 123,
                "max_weight": 'INVALID',
                "max_capacity": 'INVALID'
            }
        )
        msg = {'Errors': {'id': ['Missing data for required field.'],
                          'max_capacity': ['Not a valid integer.'],
                          'max_weight': ['Not a valid integer.'],
                          'address': ['Not a valid string.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.delete_one_storage',
           new=CoroutineMock(return_value={'address': '197D Klochkovska str.'}))
    def test_delete_one_storage_resource_valid(self):
        request, response = self.test_client.delete(self.url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully deleted storage 197D Klochkovska str.'})

    @patch('service_api.resources.storage_resource.delete_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_storage_resource_id_not_exist(self):
        request, response = self.test_client.delete(self.id_not_exist_url)
        msg = {'msg': 'Storage with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.delete_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_storage_resource_bad_id(self):
        request, response = self.test_client.delete(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.update_storage_by_id',
           new=CoroutineMock(return_value={'address': '56 Klochkovska str.'}))
    def test_put_storage_resource_valid(self):
        request, response = self.test_client.put(
            self.url,
            json={
                'address': '56 Klochkovska str.',
                'max_weight': 500,
                'max_capacity': 100000
            }
        )
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Storage 56 Klochkovska str. successfully updated'})

    @patch('service_api.resources.storage_resource.update_storage_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_storage_resource_id_not_exist(self):
        request, response = self.test_client.put(
            self.id_not_exist_url,
            json={
                'address': '56 Klochkovska str.',
                'max_weight': 500,
                'max_capacity': 100000
            }
        )
        msg = {'msg': 'Storage with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.update_storage_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_storage_resource_bad_types(self):
        request, response = self.test_client.put(
            self.bad_url,
            json={
                'address': 123,
                'max_weight': 'INVALID',
                'max_capacity': 'INVALID'
            }
        )
        msg = {'Errors': {'id': ['Not a valid UUID.'],
                          'max_capacity': ['Not a valid integer.'],
                          'max_weight': ['Not a valid integer.'],
                          'address': ['Not a valid string.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=one_storage))
    def test_get_storage_by_id_resource_valid(self):
        request, response = self.test_client.get(self.url)
        storage_by_id = {
            "Storage": {
                "id": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
                "address": "197D Klochkovska str.",
                "max_weight": 1000,
                "max_capacity": 30000
            }
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, storage_by_id)

    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_storage_by_id_not_exists_resource(self):
        request, response = self.test_client.get(self.id_not_exist_url)
        msg = {'msg': 'Storage with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_storage_by_id_resource_bad_id(self):
        request, response = self.test_client.get(self.bad_url)
        msg = {"Errors": {
            "_schema": [
                ["badly formed hexadecimal UUID string"]
            ]
        }}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)
