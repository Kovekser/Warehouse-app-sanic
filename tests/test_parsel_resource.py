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

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=[]))
    def test_get_all_parcel_resource_empty_table(self):
        request, response = app.test_client.get('/parcel')
        self.assertEqual(response.json, {"Parcels": []})

    @patch('service_api.resources.parcel_resource.get_all_parcels',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_parcels_resource_not_empty(self):
        row_keys = ("id", "description", "type_id", "weight", "cost", "supply_id")
        request, response = app.test_client.get('/parcel')
        self.assertGreater(len(response.json.values()), 0)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Parcels'], list)
        for row in response.json['Parcels']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.parcel_resource.insert_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_resource(self):
        request, response = app.test_client.post('/parcel')
        self.assertEqual(response.json, {'msg': 'Successfully created parcel'})

    @patch('service_api.resources.parcel_resource.delete_one_parcel',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_parcel_resource(self):
        request, response = app.test_client.delete('/parcel/d384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {'msg': 'Successfully deleted parcel'})

    @patch('service_api.resources.parcel_resource.update_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_resource(self):
        request, response = app.test_client.put('/parcel/d384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {'msg': 'Parcel d384a7d2-58a5-47f6-9f23-92b8d0d4dae8 successfully updated'})

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=one_parcel))
    def test_get_parcel_by_id_exists_resource(self):
        request, response = app.test_client.get('/parcel/d384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {"Parcel": {
            "id": "d384a7d2-58a5-47f6-9f23-92b8d0d4dae8",
            "description": "Food",
            "type_id": "d8134182-6cbf-4aba-9cbe-4a3396ad430c",
            "weight": 61,
            "cost": 16243,
            "supply_id": "3ac93c38-7114-43dd-810a-a11384be3fd8"
        }})

    @patch('service_api.resources.parcel_resource.get_parcel_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_by_id_not_exists_resource(self):
        request, response = app.test_client.get('/parcel/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {'msg': 'Parcel with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'})