from types import GeneratorType
from datetime import datetime
from freezegun import freeze_time
from unittest import TestCase, mock

from service_api.utils import path_finder
from service_api.utils.json_loader import JsonLoader
from service_api.utils.delivery_date import delivery_date


@mock.patch('service_api.utils.path_finder.os.getcwd',
            new=mock.Mock(return_value='./tests'))
class PathFinderTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_path =  "./tests/fixtures/clients.json"

    def test_find_correct_path_file_name_not_empty(self):
        test_path = path_finder.get_abs_path('clients.json')
        self.assertEqual(test_path, self.correct_path)

    def test_find_correct_path_file_name_empty(self):
        test_path = path_finder.get_abs_path()
        self.assertEqual(test_path, "./tests/fixtures/")

    def test_raise_exception_wrong_type_arg(self):
        with self.assertRaises(TypeError, msg='Integer is not valid file name'):
            path_finder.get_abs_path(1)
        with self.assertRaises(TypeError, msg='Collection is not valid file name'):
            path_finder.get_abs_path([1, 2])

    def test_wrong_path(self):
        test_path = path_finder.get_abs_path('clients')
        self.assertNotEqual(test_path, self.correct_path)

    def test_gets_correct_tab_name(self):
        tab_names = ('Parsel', 'Supply', 'Storage', 'Parseltype', 'Clients')
        test_name = path_finder.get_tab_name(self.correct_path)
        self.assertIn(test_name, tab_names)


class JsonLoaderClassTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.correct_path =  "./tests/fixtures/clients.json"

    def test_init_error_raise(self):
        with self.assertRaises(TypeError):
            JsonLoader()

    def test_json_exists_true(self):
        self.assertTrue(JsonLoader.json_exists(self.correct_path))

    def test_assert_json_not_exists(self):
        wrong_file = "./tests/fixtures/aaaa.json"
        error_msg = "File with name {} doesn't exist".format(wrong_file)
        with self.assertRaises(FileNotFoundError) as err:
            JsonLoader.json_exists(wrong_file)
        self.assertEqual(str(err.exception), error_msg)

    @mock.patch("service_api.utils.json_loader.json.load", new=mock.Mock(return_value=[]))
    def test_raise_stopiteration_empty_json(self):
        with self.assertRaises(StopIteration):
            test_json = JsonLoader(self.correct_path).loaded_json
            next(test_json)

    def test_load_json_return_gen(self):
        test_load = JsonLoader(self.correct_path).loaded_json
        self.assertIsInstance(test_load, GeneratorType)

    def test_load_json_loads_correctly(self):
        json_row = {
            "id": "31732169-9b7b-4f09-aa1b-7fecb350ab14",
            "name": "John",
            "email": "johnlara@mail.com",
            "age": 18,
            "address": "3073 Derek Drive"
        }
        test_load = JsonLoader(self.correct_path).loaded_json
        test_row = next(test_load)

        self.assertIsInstance(test_row, dict)
        self.assertEqual(test_row, json_row)


@freeze_time("2019-04-12")
class ModelDeliveryDateTestCase(TestCase):
    def test_delivery_date_in_current_month(self):
        test_delivery = delivery_date(12)
        self.assertEqual(test_delivery, datetime(2019, 4, 24))

    def test_delivery_date_in_next_month(self):
        test_delivery = delivery_date(20)
        self.assertEqual(test_delivery, datetime(2019, 5, 2))
