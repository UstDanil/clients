import os
import redis
import datetime
from uuid import uuid4
from src.database.service import get_client_by_email_from_base, get_client_by_id_from_base, create_client_in_base, \
    get_match_from_base, create_match_in_base, get_clients_list_from_base
from src.services.password_service import encrypt_password, check_password
from src.services.token_service import generate_jwt, decode_jwt
from src.services.image_service import add_watermark_to_avatar
from src.services.email_service import send_emails

redis_client = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)
MAX_MATCHES_FOR_DAY = int(os.getenv("MAXIMUM_CLIENT_MATCHES_PER_DAY"))


async def get_client_by_email(email):
    client_with_email = await get_client_by_email_from_base(email)
    return client_with_email


async def create_client(form):
    encrypted_password = encrypt_password(form["password"])
    client_password = encrypted_password.decode()
    client_id = uuid4()
    avatar_path = f"/application/static/avatar/{str(client_id)}.jpg"
    await create_client_in_base(client_id, form, client_password, avatar_path)
    await add_watermark_to_avatar(form['avatar'], avatar_path)
    jwt = generate_jwt(client_id)
    return jwt


async def authorize_client(client_id, client_password, input_password):
    is_password_valid = check_password(input_password, str.encode(client_password))
    if not is_password_valid:
        print("User with such email already exists, but password is incorrect.")
        return None
    jwt = generate_jwt(client_id)
    return jwt


async def evaluate_client(token, client_id):
    initiator_id = decode_jwt(token)
    if not initiator_id:
        return False, {"detail": "Incorrect token"}
    client = await get_client_by_id_from_base(client_id)
    if not client:
        return False, {"detail": "Matching client not found."}
    existing_match = await get_match_from_base(initiator_id, client_id)
    if existing_match:
        return False, {"detail": "This match already exists"}

    redis_key = f"{datetime.datetime.now().date()}:{str(initiator_id)}"
    if redis_client.exists(redis_key):
        matches_for_day = int(redis_client.get(redis_key).decode('utf-8'))
        if matches_for_day >= MAX_MATCHES_FOR_DAY:
            return False, {"detail": "You have reached the maximum number of matcher for the day."}
        else:
            redis_client.setex(redis_key, 60*60*24, matches_for_day+1)
    else:
        redis_client.setex(redis_key, 60*60*24, 1)
    await create_match_in_base(initiator_id, client_id)
    reverse_matching = await get_match_from_base(client_id, initiator_id)
    if reverse_matching:
        initiator = await get_client_by_id_from_base(initiator_id)
        send_emails(initiator, client)
    return True, {"detail": "OK"}


async def get_clients_list(gender, first_name, last_name, sort_by_date):
    clients = await get_clients_list_from_base(gender, first_name, last_name, sort_by_date)
    result = [
        {
            "gender": client.gender,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "avatar": client.avatar,
        } for client in clients
    ]
    return result
