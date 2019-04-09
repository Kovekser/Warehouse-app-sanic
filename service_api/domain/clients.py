import uuid

from service_api.models import Clients
from service_api.db import select, insert


async def get_all_clients():
    statement = Clients.select()
    return await select(statement)


async def get_client_by_id(client_id):
    id_ = uuid.UUID(client_id)
    statement = Clients.select().where(Clients.c.id == id_)
    return await select(statement)


async def insert_one_client(row):
    statement = Clients.insert().values(**row)
    await insert(statement)
