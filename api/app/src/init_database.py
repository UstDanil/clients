import os
from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool


class DBSettings(BaseSettings):
    DB_USERNAME: str = os.getenv('DB_USERNAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_DATABASE: str = os.getenv('DB_DATABASE')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')

    @property
    def data_source_name(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_DATABASE}"


db_settings = DBSettings()
engine = create_async_engine(db_settings.data_source_name, echo=False, poolclass=NullPool)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
