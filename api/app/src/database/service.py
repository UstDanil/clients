from src.init_database import session_maker
from src.database.repository import Repository


async def get_client_by_email_from_base(email):
    async with session_maker() as session:
        repository = Repository(session)
        client = await repository.get_client_by_email(email)
    return client


async def create_client_in_base(client_id, client_info, client_password, avatar_path):
    async with session_maker() as session:
        repository = Repository(session)
        client_id = await repository.create_client(client_id, client_info, client_password, avatar_path)
    return client_id
