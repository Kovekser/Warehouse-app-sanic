import uuid

from service_api.models import Storage
from service_api.db import select, insert


async def get_all_storage():
    statement = Storage.select()
    return await select(statement)


async def insert_one_storage(row):
    statement = Storage.insert().values(**row)
    await insert(statement)


async def get_storage_by_id(storage_id):
    id_ = uuid.UUID(storage_id)
    statement = Storage.select().where(Storage.c.id == id_)
    return await select(statement)
