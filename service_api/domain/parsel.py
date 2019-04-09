from service_api.models import Parsel
from service_api.db import select, insert


async def get_all_parsels():
    statement = Parsel.select()
    return await select(statement)

async def insert_one_parsel(row):
    statement = Parsel.insert().values(**row)
    await insert(statement)

