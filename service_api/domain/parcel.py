from service_api.models import Parcel, Clients, Storage, Supply, Parceltype
from service_api.db import select_statement, execute_statement
from sqlalchemy import select, and_


async def get_all_parcels():
    statement = Parcel.select()
    return await select_statement(statement)


async def insert_one_parcel(row):
    statement = Parcel.insert().values(**row)
    await execute_statement(statement)


async def get_parcel_by_id(parcel_id):
    statement = Parcel.select().\
        where(Parcel.c.id == parcel_id)
    return await select_statement(statement)


async def delete_one_parcel(parcel_id):
    statement = Parcel.delete().\
        where(Parcel.c.id == parcel_id).\
        returning(Parcel.c.id)
    return await select_statement(statement)


async def delete_all_parcel():
    statement = Parcel.delete()
    await execute_statement(statement)


async def update_parcel_by_id(data):
    statement = Parcel.update().\
        values(**data).\
        where(Parcel.c.id == data['id']).\
        returning(Parcel.c.id)
    return await select_statement(statement)


async def get_parcel_by_type_and_storage(parcel_type, storage, date):
    statement = ''
    if date:
        if len(date) == 1:
            date = date[0]
            statement = select([Parcel.c.id.label('parcel_id'), Parcel.c.description, Parcel.c.cost,
                                Parceltype.c.type_name, Clients.c.name.label('client_name'),
                                Storage.c.address, Supply.c.received_date]).\
                select_from(Parcel.join(Parceltype, Parcel.c.type_id == Parceltype.c.id).
                            join(Supply, Parcel.c.supply_id == Supply.c.id).
                            join(Clients, Supply.c.client_id == Clients.c.id).
                            join(Storage, Storage.c.id == Supply.c.to_storage)).\
                where(and_
                        (Parceltype.c.type_name == parcel_type,
                         Supply.c.to_storage == storage,
                         Supply.c.received_date == date
                        )
                      )
        elif len(date) == 2:
            statement = select([Parcel.c.id.label('parcel_id'), Parcel.c.description, Parcel.c.cost,
                                Parceltype.c.type_name, Clients.c.name.label('client_name'),
                                Storage.c.address, Supply.c.received_date]).\
                select_from(Parcel.join(Parceltype, Parceltype.c.id == Parcel.c.type_id).
                            join(Supply, Parcel.c.supply_id == Supply.c.id).
                            join(Clients, Supply.c.client_id == Clients.c.id).
                            join(Storage, Storage.c.id == Supply.c.to_storage)).\
                where(and_
                        (Parceltype.c.type_name == parcel_type,
                         Supply.c.to_storage == storage,
                         Supply.c.received_date.between(*sorted(date))
                        )
                      )
    else:
        statement = select([Parcel.c.id.label('parcel_id'), Parcel.c.description, Parcel.c.cost,
                            Parceltype.c.type_name, Clients.c.name.label('client_name'), Storage.c.address,
                            Supply.c.received_date]). \
            select_from(Parcel.join(Parceltype, Parceltype.c.id == Parcel.c.type_id).
                        join(Supply, Parcel.c.supply_id == Supply.c.id).
                        join(Clients, Supply.c.client_id == Clients.c.id).
                        join(Storage, Storage.c.id == Supply.c.to_storage)). \
            where(and_
                  (Parceltype.c.type_name == parcel_type,
                   Supply.c.to_storage == storage
                   )
                  )
    return await select_statement(statement)
