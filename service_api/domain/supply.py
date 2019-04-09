import uuid

from service_api.models import Supply
from service_api.db import select, execute_statement


async def get_all_supply():
    statement = Supply.select()
    return await select(statement)


async def insert_one_supply(row):
    statement = Supply.insert().values(**row)
    await execute_statement(statement)


async def get_supply_by_id(supply_id):
    id_ = uuid.UUID(supply_id)
    statement = Supply.select().where(Supply.c.id == id_)
    return await select(statement)


async def delete_one_supply(supply_id):
    id_ = uuid.UUID(supply_id)
    statement = Supply.delete().where(Supply.c.id == id_)
    await execute_statement(statement)


async def update_supply_by_id(supply_id, data):
    id_ = uuid.UUID(supply_id)
    statement = Supply.update().\
        values(**data).\
        where(Supply.c.id == id_)
    await execute_statement(statement)
