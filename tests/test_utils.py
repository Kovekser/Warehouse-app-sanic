from types import GeneratorType
from unittest import TestCase, mock

from service_api.utils import path_finder
from service_api.utils.json_loader import JsonLoader
from service_api.utils.load_json_data import get_file_list


@mock.patch('service_api.utils.path_finder.os.getcwd',
            new=mock.Mock(return_value='/home/kkovale/My_code/Warehouse-app-sanic'))
class PathFinderTestCase(TestCase):
    def setUp(self):
        self.correct_path = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/clients.json"
        self.tab_names = ('Parsel', 'Supply', 'Storage', 'Parseltype', 'Clients')

    def test_find_correct_path_file_name_not_empty(self):
        test_path = path_finder.get_abs_path('clients.json')
        self.assertEqual(test_path, self.correct_path)

    def test_find_correct_path_file_name_empty(self):
        test_path = path_finder.get_abs_path()
        self.assertEqual(test_path, "/home/kkovale/My_code/Warehouse-app-sanic/fixtures")

    def test_raise_exception_wrong_type_arg(self):
        with self.assertRaises(TypeError, msg='Integer is not valid file name'):
            path_finder.get_abs_path(1)
        with self.assertRaises(TypeError, msg='Collection is not valid file name'):
            path_finder.get_abs_path([1, 2])

    def test_wrong_path(self):
        test_path = path_finder.get_abs_path('clients')
        self.assertNotEqual(test_path, self.correct_path)

    def test_gets_correct_tab_name(self):
        test_name = path_finder.get_tab_name(self.correct_path)
        self.assertIn(test_name, self.tab_names)


class JsonLoaderClassTestCase(TestCase):
    def setUp(self):
        self.file = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/clients.json"
        self.wrong_file = "/home/kkovale/My_code/Warehouse-app-sanic/fixtures/aaaa.json"
        self.error_msg = "File with name {} doesn't exist".format(self.wrong_file)
        self.json_row = {
                          "name": "John",
                          "email": "johnlara@mail.com",
                          "age": 18,
                          "address": "3073 Derek Drive"
                        }

    def test_init_error_raise(self):
        with self.assertRaises(TypeError):
            JsonLoader()

    def test_json_exists_true(self):
        self.assertTrue(JsonLoader.json_exists(self.file))

    def test_assert_json_not_exists(self):
        with self.assertRaises(FileNotFoundError) as err:
            JsonLoader.json_exists(self.wrong_file)
        self.assertEqual(str(err.exception), self.error_msg)

    @mock.patch("service_api.utils.json_loader.json.load", new=mock.Mock(return_value=[]))
    def test_raise_stopiteration_empty_json(self):
        with self.assertRaises(StopIteration):
            test_json = JsonLoader(self.file).loaded_json
            next(test_json)

    def test_load_json_return_gen(self):
        test_load = JsonLoader(self.file).loaded_json
        self.assertIsInstance(test_load, GeneratorType)

    def test_load_json_loads_correctly(self):
        test_load = JsonLoader(self.file).loaded_json
        test_row = next(test_load)
        self.assertIsInstance(test_row, dict)
        self.assertEqual(test_row, self.json_row)

# class LoadJsonDataCmdLineTestCase(TestCase):
#     all_files = ['clients.json', 'parsel.json', 'parseltype.json', 'storage.json', 'supply.json']
#     def setUp(self):
#         self.not_all_files = ['clients.json', 'parsel.json']
#
#     @mock.patch('service_api.utils.load_json_data.os.listdir', new=mock.Mock(return_value=all_files))
#     def test_get_file_list_all_files(self):
#         self.assertEqual()

# Here i have a HUUUGEEE blocker


# TODO get_file_list - mock get_abs_path. 2 cases: all files, not all files
# TODO get_dict_gen - returns dict, case where all files dict, case where not all files dict
