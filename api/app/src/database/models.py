from uuid import uuid4
from sqlalchemy import MetaData, Column, String, ForeignKey
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base

Base = declarative_base(metadata=MetaData())


class Client(Base):
    __tablename__ = 'clients'

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid4())
    gender = Column(String(), nullable=False)
    first_name = Column(String(), nullable=False)
    last_name = Column(String(), nullable=False)
    email = Column(String(), nullable=False, unique=True)
    password = Column(String(), nullable=False)
    avatar = Column(String(), nullable=False)


class Match(Base):
    __tablename__ = 'matches'

    initiator_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Client.id, ondelete="CASCADE"), nullable=False, primary_key=True)
    client_id = Column(postgresql.UUID(as_uuid=True), ForeignKey(Client.id, ondelete="CASCADE"), nullable=False, primary_key=True)
