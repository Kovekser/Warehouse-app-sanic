import uuid

from service_api.models import Parsel
from service_api.db import select, execute_statement


async def get_all_parsels():
    statement = Parsel.select()
    return await select(statement)


async def insert_one_parsel(row):
    statement = Parsel.insert().values(**row)
    await execute_statement(statement)


async def get_parsel_by_id(parsel_id):
    id_ = uuid.UUID(parsel_id)
    statement = Parsel.select().where(Parsel.c.id == id_)
    return await select(statement)


async def delete_one_parsel(parsel_id):
    id_ = uuid.UUID(parsel_id)
    statement = Parsel.delete().where(Parsel.c.id == id_)
    await execute_statement(statement)


async def update_parsel_by_id(parsel_id, data):
    id_ = uuid.UUID(parsel_id)
    statement = Parsel.update().\
        values(**data).\
        where(Parsel.c.id == id_)
    await execute_statement(statement)
