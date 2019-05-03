from service_api.models import Clients
from service_api.db import select, execute_statement
from service_api.constants import DB_CONFIG


async def get_all_clients(db=DB_CONFIG):
    statement = Clients.select()
    return await select(statement, db)


async def get_client_by_id(client_id, db=DB_CONFIG):
    statement = Clients.select().where(Clients.c.id == client_id)
    return await select(statement, db)


async def insert_one_client(row, db=DB_CONFIG):
    statement = Clients.insert().values(**row)
    await execute_statement(statement, db)


async def delete_one_client(client_id, db=DB_CONFIG):
    statement = Clients.delete(). \
        where(Clients.c.id == client_id). \
        returning(Clients.c.email)
    return await select(statement, db)


async def delete_all_clients(db=DB_CONFIG):
    statement = Clients.delete()
    await execute_statement(statement, db)


async def update_client_by_id(data, db=DB_CONFIG):
    statement = Clients.update().\
        values(**data).\
        where(Clients.c.id == data['id']). \
        returning(Clients.c.email)
    return await select(statement, db)
