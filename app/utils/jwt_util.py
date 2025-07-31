import jwt
import datetime
import os
from fastapi import HTTPException

def encode_auth_token(user_id, fin_kod, profile_completed, role, secret_key=None):
    # In FastAPI, user fetching should be done outside, so remove User.query here
    if secret_key is None:
        secret_key = os.getenv('SECRET_KEY')
    if not secret_key or not isinstance(secret_key, str):
        raise ValueError("SECRET_KEY is missing or not a valid string")

    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        'sub': str(user_id),
        'fin_kod': str(fin_kod),
        'profile_completed': str(profile_completed),
        'role': role,
        'exp': expiration_time
    }

    token = jwt.encode(payload, secret_key, algorithm='HS256')
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def decode_auth_token(auth_token, secret_key=None):
    try:
        if secret_key is None:
            secret_key = os.getenv('SECRET_KEY')
        if not secret_key or not isinstance(secret_key, str):
            raise ValueError("SECRET_KEY is missing or not a valid string")

        payload = jwt.decode(auth_token, secret_key, algorithms=['HS256'], options={"require": ["exp"]})

        return {
            'user_id': payload['sub'],
            'fin_kod': payload['fin_kod'],
            'profile_completed': payload['profile_completed'],
            'role': payload['role']
        }

    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None
