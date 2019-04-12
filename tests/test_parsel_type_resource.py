import json
from asynctest import TestCase, CoroutineMock, patch

from service_api.application import app


class ParcelTypeResourceTestCase(TestCase):
    with open('./tests/fixtures/parceltype.json') as f:
        select_all_data = json.load(f)
    one_parcel_type = {
        "id": "f538ef51-c3f9-4fa9-a539-ca49c5fc81a8",
        "type_name": "letter"
    }

    @patch('service_api.resources.parceltype_resource.get_all_types',
           new=CoroutineMock(return_value=[]))
    def test_get_all_parceltype_resource_empty_table(self):
        request, response = app.test_client.get('/parceltype')
        self.assertEqual(response.json, {'Types': []})

    @patch('service_api.resources.parceltype_resource.get_all_types',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_parcel_types_resource_not_empty(self):
        row_keys = ("id", "type_name")
        request, response = app.test_client.get('/parceltype')
        self.assertGreater(len(response.json.values()), 0)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Types'], list)
        for row in response.json['Types']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource(self):
        request, response = app.test_client.post('/parceltype')
        self.assertEqual(response.json, {'msg': 'Successfully created parcel type'})

    @patch('service_api.resources.parceltype_resource.delete_one_type',
           new=CoroutineMock(return_value=[]))
    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=one_parcel_type))
    def test_delete_one_parcel_type_resource(self):
        request, response = app.test_client.delete('/parceltype/f538ef51-c3f9-4fa9-a539-ca49c5fc81a8')
        self.assertEqual(response.json, {'msg': 'Successfully deleted parcel type letter'})

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value=[]))
    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=one_parcel_type))
    def test_put_parcel_type_resource(self):
        request, response = app.test_client.put('/parceltype/f538ef51-c3f9-4fa9-a539-ca49c5fc81a8')
        self.assertEqual(response.json, {'msg': 'Parcel type letter successfully updated'})

    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=one_parcel_type))
    def test_get_parcel_type_by_id_exists_resource(self):
        request, response = app.test_client.get('/parceltype/f538ef51-c3f9-4fa9-a539-ca49c5fc81a8')
        self.assertEqual(response.json, {"Parcel_type": {
            "id": "f538ef51-c3f9-4fa9-a539-ca49c5fc81a8",
            "type_name": "letter"
        }})

    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_type_by_id_not_exists_resource(self):
        request, response = app.test_client.get('/parceltype/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        self.assertEqual(response.json, {'msg': 'Parcel type with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'})