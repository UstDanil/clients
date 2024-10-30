from src.init_database import session_maker
from src.database.repository import Repository


async def get_client_by_email_from_base(email):
    async with session_maker() as session:
        repository = Repository(session)
        client = await repository.get_client_by_email(email)
    return client


async def get_client_by_id_from_base(client_id):
    async with session_maker() as session:
        repository = Repository(session)
        client = await repository.get_client_by_id(client_id)
    return client


async def create_client_in_base(client_id, client_info, client_password, avatar_path):
    async with session_maker() as session:
        repository = Repository(session)
        await repository.create_client(client_id, client_info, client_password, avatar_path)


async def get_match_from_base(initiator_id, client_id):
    async with session_maker() as session:
        repository = Repository(session)
        existing_match = await repository.get_match(initiator_id, client_id)
    return existing_match


async def create_match_in_base(initiator_id, client_id):
    async with session_maker() as session:
        repository = Repository(session)
        await repository.create_match(initiator_id, client_id)


async def get_clients_list_from_base(gender, first_name, last_name, sort_by_date):
    async with session_maker() as session:
        repository = Repository(session)
        clients = await repository.get_clients(gender, first_name, last_name, sort_by_date)
    return clients
