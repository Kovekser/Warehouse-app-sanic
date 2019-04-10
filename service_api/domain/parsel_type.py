import uuid

from service_api.models import Parseltype
from service_api.db import select, execute_statement


async def get_all_types():
    statement = Parseltype.select()
    return await select(statement)


async def insert_one_type(row):
    statement = Parseltype.insert().values(**row)
    await execute_statement(statement)


async def get_type_by_id(type_id):
    id_ = uuid.UUID(type_id)
    statement = Parseltype.select().where(Parseltype.c.id == id_)
    return await select(statement)


async def delete_one_type(type_id):
    id_ = uuid.UUID(type_id)
    statement = Parseltype.delete().where(Parseltype.c.id == id_)
    await execute_statement(statement)


async def update_type_by_id(type_id, data):
    id_ = uuid.UUID(type_id)
    statement = Parseltype.update().\
        values(**data).\
        where(Parseltype.c.id == id_)
    await execute_statement(statement)
