import os
import asyncio

from service_api.utils.json_loader import JsonLoader
from service_api.utils.path_finder import get_abs_path, get_tab_name
from service_api.domain.clients import insert_one_client
from service_api.domain.parsel import insert_one_parsel
from service_api.domain.parsel_type import insert_one_type
from service_api.domain.storage import insert_one_storage
from service_api.domain.supply import insert_one_supply


models_dict = {'Clients': insert_one_client,
               'Parsel': insert_one_parsel,
               'Parseltype': insert_one_type,
               'Storage': insert_one_storage,
               'Supply': insert_one_supply}


async def load_json_data(data: dict):
    for model, json_list in data.items():
        for row in json_list:
            await models_dict[model](row)


def run_loop(coro, data):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro(data))
    loop.close()


def get_file_list(parsed_args):
    if parsed_args.all:
        file_list = [get_abs_path(f) for f in os.listdir(get_abs_path())]
    else:
        file_list = [get_abs_path(f) for f in parsed_args.table]
    return file_list


def get_dict_gen(files):
    return {get_tab_name(f): JsonLoader(f).loaded_json
            for f in files}


def load_fixtures(cmd_args):
    file_list = get_file_list(cmd_args)
    data = get_dict_gen(file_list)
    run_loop(load_json_data, data)
