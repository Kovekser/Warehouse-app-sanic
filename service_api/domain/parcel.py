from service_api.models import Parcel, Clients, Storage, Supply, Parceltype
from service_api.db import select_statement, execute_statement
from sqlalchemy import select, and_, func


async def get_all_parcels():
    statement = Parcel.select()
    return await select_statement(statement)


async def insert_one_parcel(row):
    statement = Parcel.insert().values(**row)
    await execute_statement(statement)


async def get_parcel_by_id(parcel_id):
    statement = Parcel.select(). \
        where(Parcel.c.id == parcel_id)
    return await select_statement(statement)


async def delete_one_parcel(parcel_id):
    statement = Parcel.delete(). \
        where(Parcel.c.id == parcel_id). \
        returning(Parcel.c.id)
    return await select_statement(statement)


async def delete_all_parcel():
    statement = Parcel.delete()
    await execute_statement(statement)


async def update_parcel_by_id(data):
    statement = Parcel.update(). \
        values(**data). \
        where(Parcel.c.id == data['id']). \
        returning(Parcel.c.id)
    return await select_statement(statement)


async def get_parcel_by_type_and_storage(parcel_type, storage, date):
    statement = ''
    base_statement = select([Parcel.c.id.label('parcel_id'), Parcel.c.description, Parcel.c.cost,
                             Parceltype.c.type_name, Clients.c.name.label('client_name'),
                             Storage.c.address, Supply.c.received_date]). \
        select_from(Parcel.join(Parceltype, Parcel.c.type_id == Parceltype.c.id).
                    join(Supply, Parcel.c.supply_id == Supply.c.id).
                    join(Clients, Supply.c.client_id == Clients.c.id).
                    join(Storage, Storage.c.id == Supply.c.to_storage))
    if date:
        if len(date) == 1:
            statement = base_statement.where(and_
                                             (Parceltype.c.type_name == parcel_type,
                                              Supply.c.to_storage == storage,
                                              Supply.c.received_date == date[0])
                                             ).alias("select_statement")
        elif len(date) == 2:
            statement = base_statement.where(and_
                                             (Parceltype.c.type_name == parcel_type,
                                              Supply.c.to_storage == storage,
                                              Supply.c.received_date.between(*sorted(date)))
                                             ).alias("select_statement")
    else:
        statement = base_statement.where(and_
                                         (Parceltype.c.type_name == parcel_type,
                                          Supply.c.to_storage == storage)).alias("select_statement")

    sum_stmt = select([func.sum(statement.c.cost).label('total_cost')])

    return await select_statement(statement), await select_statement(sum_stmt)
