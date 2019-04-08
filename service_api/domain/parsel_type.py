from service_api.models import Parseltype
from service_api.db import select, insert


async def get_all_types():
    statement = Parseltype.select()
    return await select(statement)


async def insert_one(row):
    statement = Parseltype.insert().values(**row)
    await insert(statement)
