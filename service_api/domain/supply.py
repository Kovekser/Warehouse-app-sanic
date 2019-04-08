from service_api.models import Supply
from service_api.db import select, insert


async def get_all_supply():
    statement = Supply.select()
    return await select(statement)

async def insert_one(row):
    statement = Supply.insert().values(**row)
    await insert(statement)
