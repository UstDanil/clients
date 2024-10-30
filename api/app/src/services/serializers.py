import re
from src.services.token_service import decode_jwt
from src.database.service import get_client_by_id_from_base

SIGNUP_FIELDS = ['gender', 'first_name', 'last_name', 'avatar', 'latitude', 'longitude']
AVAILABLE_GENDER = ['male', 'female']


def validate_email(email):
    email_validate_pattern = r"^\S+@\S+\.\S+$"
    is_valid = bool(re.match(email_validate_pattern, email))
    return is_valid


def validate_user_creation_data(form):
    if any([bool(field not in form.keys()) for field in SIGNUP_FIELDS]):
        return False, {"detail": "Incorrect fields for user creating. "
                                 "Send fields: email, password, gender, first_name, last_name, "
                                 "avatar, latitude, longitude."}
    if form['gender'].lower() not in AVAILABLE_GENDER:
        return False, {"detail": "Incorrect gender. Available: male or female."}
    try:
        float(form['latitude'])
        if float(form['latitude']) < 40 or float(form['latitude']) > 78:
            return False, {"detail": "Incorrect latitude. Available: from 40 to 78 with decimal."}
    except ValueError:
        return False, {"detail": "Incorrect latitude. Floating point number expected (with . )."}
    try:
        float(form['longitude'])
        if float(form['longitude']) < 19 or float(form['longitude']) > 180:
            return False, {"detail": "Incorrect latitude. Available: from 18 to 180 with decimal."}
    except ValueError:
        return False, {"detail": "Incorrect longitude. Floating point number expected (with . )."}
    return True, {"detail": "OK"}


async def validate_token(token):
    initiator_id = decode_jwt(token)
    if not initiator_id:
        return False, None
    initiator = await get_client_by_id_from_base(initiator_id)
    if not initiator:
        return False, None
    return True, initiator
