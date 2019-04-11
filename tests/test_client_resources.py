from unittest.mock import Mock, patch
from unittest import TestCase

from service_api.resources.smokeview import SmokeResource
from service_api.resources.client_resource import ClientAllResource, ClientResource


class ClientResourceTestCase(TestCase):

     @patch('service_api.resources.client_resource.get_all_clients', new=Mock(return_value=[]))
     def test_get_all_clients_empty_clients(self):
          response = testClient.get('/client')
          self.asserEqual({"Clients": []}, response)

     @patch('service_api.resources.client_resource.get_all_clients', new=Mock(return_value=[{'okey'}]))
     def test_get_all_clients_empty_clients(self):
          response = testClient.get('/client')
          self.asserEqual({"Clients": [{'okey'}]}, response)

