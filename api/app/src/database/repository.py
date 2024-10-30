import datetime
from sqlalchemy import select, func

from src.database.models import Client, Match


class Repository:
    def __init__(self, session):
        self.session = session
        self.model_client = Client
        self.model_match = Match

    async def get_client_by_email(self, email):
        query = select(self.model_client).where(self.model_client.email == email)
        result = await self.session.execute(query)
        return result.scalar()

    async def get_client_by_id(self, client_id):
        query = select(self.model_client).where(self.model_client.id == client_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def create_client(self, client_id, client_info, client_password, avatar_path):
        new_client = self.model_client(
            id=client_id,
            gender=client_info["gender"].lower(),
            first_name=client_info["first_name"],
            last_name=client_info["last_name"],
            email=client_info["email"],
            password=client_password,
            avatar=avatar_path,
            creation_date=datetime.datetime.now()
        )
        self.session.add(new_client)
        await self.session.commit()

    async def get_match(self, initiator_id, client_id):
        query = select(self.model_match).where(
            self.model_match.initiator_id == initiator_id,
            self.model_match.client_id == client_id
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def create_match(self, initiator_id, client_id):
        new_match = self.model_match(
            initiator_id=initiator_id,
            client_id=client_id,
        )
        self.session.add(new_match)
        await self.session.commit()

    async def get_clients(self, gender, first_name, last_name, sort_by_date):
        query = select(self.model_client)
        if gender:
            query = query.where(func.lower(self.model_client.gender) == func.lower(gender))
        if first_name:
            first_name_str = f"%{first_name.lower()}%"
            query = query.where(self.model_client.first_name.ilike(first_name_str))
        if last_name:
            last_name_str = f"%{last_name.lower()}%"
            query = query.where(self.model_client.last_name.ilike(last_name_str))
        if sort_by_date:
            query = query.order_by(self.model_client.creation_date.desc())
        result = await self.session.execute(query)
        return result.scalars().all()
