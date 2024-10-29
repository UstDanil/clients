from uuid import uuid4
from sqlalchemy import select

from src.database.models import Client


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_client = Client

    async def get_client_by_email(self, email):
        query = select(self.model_client).where(self.model_client.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_client(self, client_id, client_info, client_password, avatar_path):
        new_client = self.model_client(
            id=client_id,
            gender=client_info["gender"],
            first_name=client_info["first_name"],
            last_name=client_info["last_name"],
            email=client_info["email"],
            password=client_password,
            avatar=avatar_path
        )
        self.session.add(new_client)
        await self.session.commit()
