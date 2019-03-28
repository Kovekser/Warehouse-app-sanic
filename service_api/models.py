import uuid

from decimal import Decimal

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String,
    Integer,
    DateTime
)

from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

Clients = Table(
    "clients", metadata,
    Column('client_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('client_name', String, nullable=False),
    Column('email', String, nullable=False),
    Column('client_age', Integer, nullable=False),
    Column('client_address', String, nullable=False),
)

ParselType = Table(
    "parseltype", metadata,
    Column('type_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('type_name', String, nullable=False)
)

Storage = Table(
    'storage', metadata,
    Column('storage_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('address', String, nullable=False),
    Column('max_weight', Integer, nullable=False),
    Column('max_capacity', Integer, nullable=False)
)

Supply = Table(
    'supply', metadata,
    Column('supply_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('from_storage', UUID(as_uuid=True), ForeignKey('storage.storage_id', ondelete="CASCADE")),
    Column('to_storage', UUID(as_uuid=True), ForeignKey('storage.storage_id', ondelete="CASCADE")),
    Column('status', String, nullable=False),
    Column('client_id', UUID(as_uuid=True), ForeignKey('clients.client_id', ondelete="CASCADE")),
    Column('send_date', DateTime, nullable=False),
    Column('received_date', DateTime, nullable=False),
)

Parsel = Table(
    'parsel', metadata,
    Column('pars_id', UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
    Column('description', String, nullable=False),
    Column('type_id', UUID(as_uuid=True), ForeignKey('parseltype.type_id', ondelete="CASCADE")),
    Column('weight', Integer, nullable=False),
    Column('cost', Decimal, nullable=False),
    Column('supply_id', UUID(as_uuid=True), ForeignKey('supply.supply_id', ondelete="CASCADE"))
)

models = (Parsel, Supply, Storage, ParselType, Clients)