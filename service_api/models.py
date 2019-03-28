import uuid

from sqlalchemy import (
    Table,
    Column,
    MetaData,
    String,
    Integer
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

