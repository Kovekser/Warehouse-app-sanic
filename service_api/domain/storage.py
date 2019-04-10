import uuid

from service_api.models import Storage
from service_api.db import select, execute_statement


async def get_all_storage():
    statement = Storage.select()
    return await select(statement)


async def insert_one_storage(row):
    statement = Storage.insert().values(**row)
    await execute_statement(statement)


async def get_storage_by_id(storage_id):
    id_ = uuid.UUID(storage_id)
    statement = Storage.select().where(Storage.c.id == id_)
    return await select(statement)


async def delete_one_storage(storage_id):
    id_ = uuid.UUID(storage_id)
    statement = Storage.delete().where(Storage.c.id == id_)
    await execute_statement(statement)


async def update_storage_by_id(storage_id, data):
    id_ = uuid.UUID(storage_id)
    statement = Storage.update().\
        values(**data).\
        where(Storage.c.id == id_)
    await execute_statement(statement)
