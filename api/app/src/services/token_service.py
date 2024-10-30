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


def decode_jwt(token):
    try:
        payload = jwt.decode(token, key=os.getenv("API_JWT_SECRET"), algorithms=[os.getenv("API_JWT_ALGORITHM"), ])
        return payload["sub"]
    except ExpiredSignatureError:
        print("Token expired.")
        return None
    except Exception as e:
        print(e)
        return None
