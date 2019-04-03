import json
# import os

# os.chdir("../..")

class JsonLoader:
    def __init__(self, json_file):
        self.json_file = json_file

    @property
    def loaded_json(self):
        with open(self.json_file) as f:
            self._data = json.load(f)
        yield from self._data.items()

# file_name = "fixtures/clients.json"
#
# json_clients = JsonLoader(file_name)
# fff = json_clients.loaded_json
# print(next(fff))
# print(next(fff))
