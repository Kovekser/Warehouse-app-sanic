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

    @classmethod
    def setUpClass(cls):
        cls.url = '/parceltype/f538ef51-c3f9-4fa9-a539-ca49c5fc81a8'

    @patch('service_api.resources.parceltype_resource.get_all_types',
           new=CoroutineMock(return_value=[]))
    def test_get_all_parceltype_resource_empty_table(self):
        request, response = app.test_client.get('/parceltype')
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'Types': []})

    @patch('service_api.resources.parceltype_resource.get_all_types',
           new=CoroutineMock(return_value=select_all_data))
    def test_get_all_parcel_types_resource_not_empty(self):
        row_keys = ("id", "type_name")
        request, response = app.test_client.get('/parceltype')

        self.assertEqual(response.status, 200)
        self.assertIsInstance(response.json, dict)
        self.assertIsInstance(response.json['Types'], list)
        self.assertEqual(len(*response.json.values()), 5)

        for row in response.json['Types']:
            self.assertIsInstance(row, dict)
            self.assertTrue(all(map(lambda x: x in row, row_keys)))

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_valid(self):
        request, response = app.test_client.post('/parceltype', json={
            "id": "f538ef51-c3f9-4fa9-a539-ca49c5fc81a8",
            "type_name": "letter"
        })
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully created parcel type'})

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_bad_id(self):
        request, response = app.test_client.post('/parceltype', json={
            "id": "123",
            "type_name": "letter"
        })
        msg = {'Errors': {'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_no_id(self):
        request, response = app.test_client.post('/parceltype', json={
            "type_name": "letter"
        })
        msg = {'Errors': {'id': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_no_type(self):
        request, response = app.test_client.post('/parceltype', json={
            "id": "f538ef51-c3f9-4fa9-a539-ca49c5fc81a8"
        })
        msg = {'Errors': {'type_name': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_no_type_no_id(self):
        request, response = app.test_client.post('/parceltype', json={})
        msg = {'Errors': {'id': ['Missing data for required field.'],
                          'type_name': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.insert_one_type',
           new=CoroutineMock(return_value=[]))
    def test_post_one_parcel_type_resource_bad_id_no_type(self):
        request, response = app.test_client.post('/parceltype', json={
            "id": "123"
        })
        msg = {'Errors': {'id': ['Not a valid UUID.'],
                          'type_name': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.delete_one_type',
           new=CoroutineMock(return_value={'type_name': 'letter'}))
    def test_delete_one_parcel_type_resource_valid_id(self):
        request, response = app.test_client.delete(self.url)
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Successfully deleted parcel type letter'})

    @patch('service_api.resources.parceltype_resource.delete_one_type',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_parcel_type_resource_bad_id(self):
        request, response = app.test_client.delete('/parceltype/123')
        msg = {'Errors': {'_schema': [['badly formed hexadecimal UUID string']]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.delete_one_type',
           new=CoroutineMock(return_value=[]))
    def test_delete_one_parcel_type_resource_id_not_exist(self):
        request, response = app.test_client.delete('/parceltype/f123ef51-c3f9-4fa9-a539-ca49c5fc81a8')
        msg = {'msg': 'Parcel type with id f123ef51-c3f9-4fa9-a539-ca49c5fc81a8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value={'type_name': 'important letter'}))
    def test_put_parcel_type_resource_valid(self):
        request, response = app.test_client.put(self.url, json={'type_name': 'important letter'})
        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, {'msg': 'Parcel type important letter successfully updated'})

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_type_resource_bad_id(self):
        request, response = app.test_client.put('/parceltype/f123', json={'type_name': 'important letter'})
        msg = {'Errors': {'id': ['Not a valid UUID.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value=[]))
    def test_put_parcel_type_resource_id_not_exist(self):
        request, response = app.test_client.put('/parceltype/f123ef51-c3f9-4fa9-a539-ca49c5fc81a8',
                                                json={'type_name': 'important letter'})
        msg = {'msg': 'Parcel type with id f123ef51-c3f9-4fa9-a539-ca49c5fc81a8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value={'type_name': 'important letter'}))
    def test_put_parcel_type_resource_no_type(self):
        request, response = app.test_client.put(self.url, json={})
        msg = {'Errors': {'type_name': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.update_type_by_id',
           new=CoroutineMock(return_value={'type_name': 'important letter'}))
    def test_put_parcel_type_resource_no_type_bad_id(self):
        request, response = app.test_client.put('/parceltype/f123', json={})
        msg = {'Errors': {'id': ['Not a valid UUID.'],
                          'type_name': ['Missing data for required field.']}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=one_parcel_type))
    def test_get_parcel_type_by_id_exists_resource(self):
        request, response = app.test_client.get(self.url)
        type_by_id = {
            "Parcel_type": {
                "id": "f538ef51-c3f9-4fa9-a539-ca49c5fc81a8",
                "type_name": "letter"
            }
        }

        self.assertEqual(response.status, 200)
        self.assertEqual(response.json, type_by_id)

    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_type_by_id_not_exists_resource(self):
        request, response = app.test_client.get('/parceltype/f384a7d2-58a5-47f6-9f23-92b8d0d4dae8')
        msg = {'msg': 'Parcel type with id f384a7d2-58a5-47f6-9f23-92b8d0d4dae8 does not exist'}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)

    @patch('service_api.resources.parceltype_resource.get_type_by_id',
           new=CoroutineMock(return_value=[]))
    def test_get_parcel_type_by_id_resource_bad_id(self):
        request, response = app.test_client.get('/parceltype/123')
        msg = {'Errors': {'_schema': [['badly formed hexadecimal UUID string']]}}

        self.assertEqual(response.status, 404)
        self.assertEqual(response.json, msg)
