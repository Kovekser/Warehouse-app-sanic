from service_api.models import Clients
from service_api.db import select, insert


async def get_all_clients():
    statement = Clients.select()
    return await select(statement)

async def insert_one(row):
    statement = Clients.insert().values(**row)
    await insert(statement)

