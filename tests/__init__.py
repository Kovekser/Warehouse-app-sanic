from asynctest import TestCase
from service_api.application import app


class BaseTest(TestCase):

    @property
    def app(self):
        return app