from types import GeneratorType
from unittest import TestCase, mock

from service_api.utils import path_finder
from service_api.utils.json_loader import JsonLoader


@mock.patch('service_api.utils.path_finder.os.getcwd',
            new=mock.Mock(return_value='/home/kkovale/My_code/Warehouse-app-sanic'))
class PathFinderTestCase(TestCase):
    def test_find_correct_path_file_name_not_empty(self):
        correct_path = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/clients.json"
        test_path = path_finder.get_abs_path('clients.json')
        self.assertEqual(test_path, correct_path)

    def test_find_correct_path_file_name_empty(self):
        test_path = path_finder.get_abs_path()
        self.assertEqual(test_path, "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/")

    def test_raise_exception_wrong_type_arg(self):
        with self.assertRaises(TypeError, msg='Integer is not valid file name'):
            path_finder.get_abs_path(1)
        with self.assertRaises(TypeError, msg='Collection is not valid file name'):
            path_finder.get_abs_path([1, 2])

    def test_wrong_path(self):
        test_path = path_finder.get_abs_path('clients')
        correct_path = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/clients.json"
        self.assertNotEqual(test_path, correct_path)

    def test_gets_correct_tab_name(self):
        tab_names = ('Parsel', 'Supply', 'Storage', 'Parseltype', 'Clients')
        correct_path = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/clients.json"
        test_name = path_finder.get_tab_name(correct_path)
        self.assertIn(test_name, tab_names)


class JsonLoaderClassTestCase(TestCase):
    def test_init_error_raise(self):
        with self.assertRaises(TypeError):
            JsonLoader()

    def test_json_exists_true(self):
        file = "./fixtures/clients.json"
        self.assertTrue(JsonLoader.json_exists(file))

    def test_assert_json_not_exists(self):
        wrong_file = "./fixtures/aaaa.json"
        error_msg = "File with name {} doesn't exist".format(wrong_file)
        with self.assertRaises(FileNotFoundError) as err:
            JsonLoader.json_exists(wrong_file)
        self.assertEqual(str(err.exception), error_msg)

    @mock.patch("service_api.utils.json_loader.json.load", new=mock.Mock(return_value=[]))
    def test_raise_stopiteration_empty_json(self):
        file = "./fixtures/clients.json"
        with self.assertRaises(StopIteration):
            test_json = JsonLoader(file).loaded_json
            next(test_json)

    def test_load_json_return_gen(self):
        file = "./fixtures/clients.json"
        test_load = JsonLoader(file).loaded_json
        self.assertIsInstance(test_load, GeneratorType)

    def test_load_json_loads_correctly(self):
        file = "./fixtures/clients.json"
        json_row = {
            "name": "John",
            "email": "johnlara@mail.com",
            "age": 18,
            "address": "3073 Derek Drive"}
        test_load = JsonLoader(file).loaded_json
        test_row = next(test_load)
        self.assertIsInstance(test_row, dict)
        self.assertEqual(test_row, json_row)
