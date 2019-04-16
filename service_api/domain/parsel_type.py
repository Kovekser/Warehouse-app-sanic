import uuid

from service_api.models import Parceltype
from service_api.db import select, execute_statement


async def get_all_types():
    statement = Parceltype.select()
    return await select(statement)


async def insert_one_type(row):
    statement = Parceltype.insert().values(**row)
    await execute_statement(statement)


async def get_type_by_id(type_id):
    id_ = uuid.UUID(type_id)
    statement = Parceltype.select().where(Parceltype.c.id == id_)
    return await select(statement)


async def delete_one_type(type_id):
    id_ = uuid.UUID(type_id)
    statement = Parceltype.delete().where(Parceltype.c.id == id_)
    await execute_statement(statement)


async def update_type_by_id(type_id, data):
    id_ = uuid.UUID(type_id)
    statement = Parceltype.update().\
        values(**data).\
        where(Parceltype.c.id == id_)
    await execute_statement(statement)
