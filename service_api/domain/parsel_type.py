from service_api.models import Parceltype
from service_api.db import select, execute_statement


async def get_all_types():
    statement = Parceltype.select()
    return await select(statement)


async def insert_one_type(row):
    statement = Parceltype.insert().values(**row)
    await execute_statement(statement)


async def get_type_by_id(type_id):
    statement = Parceltype.select().where(Parceltype.c.id == type_id)
    return await select(statement)


async def delete_one_type(type_id):
    statement = Parceltype.delete().\
        where(Parceltype.c.id == type_id).\
        returning(Parceltype.c.type_name)
    return await select(statement)


async def delete_all_type():
    statement = Parceltype.delete()
    await execute_statement(statement)


async def update_type_by_id(data):
    statement = Parceltype.update().\
        values(**data).\
        where(Parceltype.c.id == data['id']). \
        returning(Parceltype.c.type_name)
    return await select(statement)
