from asynctest import TestCase

from service_api.application import app


class BaseTestCase(TestCase):

    @property
    def test_client(self):
        return app.test_client
