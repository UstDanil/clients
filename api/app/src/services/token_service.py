import os
import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta


def generate_jwt(user_id):
    payload = dict()
    payload["type"] = "access_token"
    payload["exp"] = datetime.now() + timedelta(minutes=int(os.getenv("API_JWT_ACCESS_TOKEN_EXPIRE_MINUTES")))
    payload["iat"] = datetime.now()
    payload["sub"] = str(user_id)
    return jwt.encode(payload, os.getenv("API_JWT_SECRET"), algorithm=os.getenv("API_JWT_ALGORITHM"))
