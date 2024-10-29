from uuid import uuid4
from src.database.service import get_client_by_email_from_base, create_client_in_base
from src.services.password_service import encrypt_password, check_password
from src.services.token_service import generate_jwt
from src.services.image_service import add_watermark_to_avatar


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
