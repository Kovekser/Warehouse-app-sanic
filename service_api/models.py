import uuid
from datetime import datetime
from random import randint

from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    MetaData,
    String,
    Integer,
    DateTime,
    DECIMAL
)

from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()
delivery_len = randint(3, 20)


def delivery_date(length):
    now_date = datetime.utcnow()
    day_sum = now_date.day + delivery_len
    if day_sum > 30:
        delivery_date = now_date.replace(month=now_date.month+1, day=(day_sum-30))
    else:
        delivery_date = now_date.replace(day=now_date.day + length)
    return delivery_date


Clients = Table(
    "clients", metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('age', Integer, nullable=False),
    Column('address', String, nullable=False),
)

Parseltype = Table(
    "parseltype", metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('type_name', String, nullable=False)
)

Storage = Table(
    'storage', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('address', String, nullable=False),
    Column('max_weight', Integer, nullable=False),
    Column('max_capacity', Integer, nullable=False)
)

Supply = Table(
    'supply', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('from_storage', UUID(as_uuid=True), ForeignKey('storage.id', ondelete="CASCADE")),
    Column('to_storage', UUID(as_uuid=True), ForeignKey('storage.id', ondelete="CASCADE")),
    Column('status', String, nullable=False),
    Column('client_id', UUID(as_uuid=True), ForeignKey('clients.id', ondelete="CASCADE")),
    Column('send_date', DateTime, nullable=False, default=datetime.utcnow()),
    Column('received_date', DateTime, nullable=False, default=delivery_date(delivery_len)),
)

Parsel = Table(
    'parsel', metadata,
    Column('id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('description', String, nullable=False),
    Column('type_id', UUID(as_uuid=True), ForeignKey('parseltype.id', ondelete="CASCADE")),
    Column('weight', DECIMAL, nullable=False),
    Column('cost', DECIMAL, nullable=False),
    Column('supply_id', UUID(as_uuid=True), ForeignKey('supply.id', ondelete="CASCADE"))
)

models = (Parsel, Supply, Storage, Parseltype, Clients)
