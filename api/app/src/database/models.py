from uuid import uuid4
from sqlalchemy import MetaData, Column, String
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
