import asyncio
from fastapi.testclient import TestClient
from unittest.mock import patch
from PIL import Image
from sqlalchemy import text

from src.main import app
from src.init_database import session_maker
from src.services.token_service import generate_jwt


client = TestClient(app)


async def mock_create_client(self, client_id, client_info, client_password, avatar_path):
    pass


async def mock_create_match(self, initiator_id, client_id):
    pass


@patch("src.database.repository.Repository.create_client", mock_create_client)
def test_create_client_bad_gender():
    img = Image.new('RGB', (200, 200), 'black')
    img.save('test1.jpg')
    client_data = {
        "gender": "1345",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@rambler.ru",
        "password": "client_password",
        "latitude": 54.53,
        "longitude": 37.654
    }
    with open('test1.jpg', "rb") as f:
        files = {"avatar": ("avatar", f, "multipart/form-data")}
        response = client.post("/api/clients/create", data=client_data, files=files)
        assert response.status_code == 400


@patch("src.database.repository.Repository.create_client", mock_create_client)
def test_create_client_no_avatar():
    client_data = {
        "gender": "1345",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@rambler.ru",
        "password": "client_password",
        "latitude": 54.53,
        "longitude": 37.654
    }
    response = client.post("/api/clients/create", data=client_data)
    assert response.status_code == 400


@patch("src.database.repository.Repository.create_client", mock_create_client)
def test_create_client_bad_email():
    client_data = {
        "gender": "1345",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "erambler.ru",
        "password": "client_password",
        "latitude": 54.53,
        "longitude": 37.654
    }
    response = client.post("/api/clients/create", data=client_data)
    assert response.status_code == 400


@patch("src.database.repository.Repository.create_client", mock_create_client)
def test_create_client_correct():
    img = Image.new('RGB', (200, 200), 'black')
    img.save('test1.jpg')
    client_data = {
        "gender": "male",
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@rambler.ru",
        "password": "client_password",
        "latitude": 54.53,
        "longitude": 37.654
    }
    with open('test1.jpg', "rb") as f:
        files = {"avatar": ("avatar", f, "multipart/form-data")}
        response = client.post("/api/clients/create", data=client_data, files=files)
        assert response.status_code == 201


@patch("src.database.repository.Repository.create_match", mock_create_match)
def test_match():
    async def get_first_match_from_base():
        async with session_maker() as session:
            first_match_in_base = await session.execute(text('SELECT * FROM matches LIMIT 1'))
            return first_match_in_base.first()

    loop = asyncio.get_event_loop()
    existing_match = loop.run_until_complete(get_first_match_from_base())
    initiator_id = existing_match[0]
    client_id = existing_match[1]
    jwt = generate_jwt(initiator_id)
    response = client.post(f"/api/clients/{str(client_id)}/match", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 400
    response = client.post(f"/api/clients/{str(client_id)}/match")
    assert response.status_code == 401


# @patch("src.database.repository.Repository.create_match", mock_create_match)
def test_clients_list():
    async def get_first_client_from_base():
        async with session_maker() as session:
            first_client_in_base = await session.execute(text('SELECT * FROM clients LIMIT 1'))
            return first_client_in_base.first()

    loop = asyncio.get_event_loop()
    first_client = loop.run_until_complete(get_first_client_from_base())
    client_id = first_client[0]
    jwt = generate_jwt(client_id)
    response = client.get(f"/api/list", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = client.get(f"/api/list")
    assert response.status_code == 401

    params = {
        "sort_by_date": True,
        "distance": 100,
        "gender": "Male"
    }
    response = client.get(f"/api/list", headers={"Authorization": f"Bearer {jwt}"}, params=params)
    assert response.status_code == 200

    params = {
        "sort_by_date": True,
        "distance": "invalid",
        "gender": 111
    }
    response = client.get(f"/api/list", headers={"Authorization": f"Bearer {jwt}"}, params=params)
    assert response.status_code == 422
