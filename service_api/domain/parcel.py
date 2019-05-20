from service_api.models import Parcel
from service_api.db import select, execute_statement


async def get_all_parcels():
    statement = Parcel.select()
    return await select(statement)


async def insert_one_parcel(row):
    statement = Parcel.insert().values(**row)
    await execute_statement(statement)


async def get_parcel_by_id(parcel_id):
    statement = Parcel.select().\
        where(Parcel.c.id == parcel_id)
    return await select(statement)


async def delete_one_parcel(parcel_id):
    statement = Parcel.delete().\
        where(Parcel.c.id == parcel_id).\
        returning(Parcel.c.id)
    return await select(statement)


async def delete_all_parcel():
    statement = Parcel.delete()
    await execute_statement(statement)


async def update_parcel_by_id(data):
    statement = Parcel.update().\
        values(**data).\
        where(Parcel.c.id == data['id']).\
        returning(Parcel.c.id)
    return await select(statement)
