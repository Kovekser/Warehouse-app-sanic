import json
from asynctest import TestCase, CoroutineMock, patch

from service_api.application import app


class StorageResourceTestCase(TestCase):
    with open('./tests/fixtures/storage.json') as f:
        select_all_data = json.load(f)
    one_storage = {
        "id": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
        "address": "197D Klochkovska str.",
        "max_weight": 1000,
        "max_capacity": 30000
    }

    @patch('service_api.resources.storage_resource.get_all_storage',
           new=CoroutineMock(return_value=[]))
    def test_get_all_storage_resource_empty_table(self):
        request, response = app.test_client.get('/storage')
        self.assertEqual(response.json, {"Storages": []})

    @patch('service_api.resources.storage_resource.get_all_storage',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_storages_resource_not_empty(self):
        row_keys = ("id", "address", "max_weight", "max_capacity")
        request, response = app.test_client.get('/storage')
        self.assertGreater(len(response.json.values()), 0)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Storages'], list)
        for row in response.json['Storages']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.storage_resource.insert_one_storage',
           new=CoroutineMock(return_value=[]))
    def test_post_one_storage_resource(self):
        request, response = app.test_client.post('/storage')
        self.assertEqual(response.json, {'msg': 'Successfully created storage'})

    @patch('service_api.resources.storage_resource.delete_one_storage',
           new=CoroutineMock(return_value=[]))
    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=one_storage))
    def test_delete_one_storage_resource(self):
        request, response = app.test_client.delete('/storage/fc6efd2d-86cb-4932-9acb-1ce97f8bb468')
        self.assertEqual(response.json, {'msg': 'Successfully deleted storage 197D Klochkovska str.'})

    @patch('service_api.resources.storage_resource.update_storage_by_id',
           new=CoroutineMock(return_value=[]))
    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=one_storage))
    def test_put_storage_resource(self):
        request, response = app.test_client.put('/storage/fc6efd2d-86cb-4932-9acb-1ce97f8bb468')
        self.assertEqual(response.json, {'msg': 'Storage 197D Klochkovska str. successfully updated'})

    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=one_storage))
    def test_get_storage_by_id_exists_resource(self):
        request, response = app.test_client.get('/storage/fc6efd2d-86cb-4932-9acb-1ce97f8bb468')
        self.assertEqual(response.json, {"Storage": {
            "id": "fc6efd2d-86cb-4932-9acb-1ce97f8bb468",
            "address": "197D Klochkovska str.",
            "max_weight": 1000,
            "max_capacity": 30000
        }})

    @patch('service_api.resources.storage_resource.get_storage_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_storage_by_id_not_exists_resource(self):
        request, response = app.test_client.get('/storage/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {'msg': 'Storage with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'})