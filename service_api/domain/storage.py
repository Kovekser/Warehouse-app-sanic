from service_api.models import Storage
from service_api.db import select, insert


async def get_all_storage():
    statement = Storage.select()
    return await select(statement)


async def insert_one_storage(row):
    statement = Storage.insert().values(**row)
    await insert(statement)
