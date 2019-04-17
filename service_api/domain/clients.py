import uuid

from service_api.models import Clients
from service_api.db import select, execute_statement


async def get_all_clients():
    statement = Clients.select()
    return await select(statement)


async def get_client_by_id(client_id):
    id_ = uuid.UUID(client_id)
    statement = Clients.select().where(Clients.c.id == id_)
    return await select(statement)


async def insert_one_client(row):
    statement = Clients.insert().values(**row)#.returning(Clients.c.email)
    await execute_statement(statement)


async def delete_one_client(client_id):
    id_ = uuid.UUID(client_id)
    statement = Clients.delete().\
        returning(Clients.c.email).\
        where(Clients.c.id == id_)
    return await select(statement)


async def update_client_by_id(data):
    # id_ = uuid.UUID(data['id'])
    statement = Clients.update().returning(Clients.c.email).\
        values(**data).\
        where(Clients.c.id == data['id'])
    return await select(statement)
