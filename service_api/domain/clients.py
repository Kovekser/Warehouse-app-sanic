from service_api.models import Clients
from service_api.db import select, execute_statement


async def get_all_clients():
    statement = Clients.select()
    return await select(statement)


async def get_client_by_id(client_id):
    statement = Clients.select().where(Clients.c.id == client_id)
    return await select(statement)


async def insert_one_client(row):
    statement = Clients.insert().values(**row)
    await execute_statement(statement)


async def delete_one_client(client_id):
    statement = Clients.delete(). \
        where(Clients.c.id == client_id). \
        returning(Clients.c.email)
    return await select(statement)


async def delete_all_clients():
    statement = Clients.delete()
    await execute_statement(statement)


async def update_client_by_id(data):
    statement = Clients.update().\
        values(**data).\
        where(Clients.c.id == data['id']). \
        returning(Clients.c.email)
    return await select(statement)
