import uuid

from service_api.models import Parseltype
from service_api.db import select, insert


async def get_all_types():
    statement = Parseltype.select()
    return await select(statement)


async def insert_one_type(row):
    statement = Parseltype.insert().values(**row)
    await insert(statement)


async def get_type_by_id(type_id):
    id_ = uuid.UUID(type_id)
    statement = Parseltype.select().where(Parseltype.c.id == id_)
    return await select(statement)
