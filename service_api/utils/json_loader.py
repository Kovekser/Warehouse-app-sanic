import json
import os


class JsonLoader:
    def __init__(self, json_file=None):
        if self.json_exists(json_file):
            self.json_file = json_file
        self._data = None

    @staticmethod
    def json_exists(file_name):
        """Function validates if requested JSON file exists"""
        if os.path.exists(file_name):
            return file_name
        else:
            raise FileNotFoundError("File with name {} doesn't exist".format(file_name))

    @property
    def loaded_json(self):
        with open(self.json_file) as f:
            self._data = json.load(f)
            yield from self._data
