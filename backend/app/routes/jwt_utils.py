from datetime import datetime, timedelta
from jose import jwt

from config import Settings

def create_access_token(data: dict, expires_delta: timedelta|None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Settings.token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.secret_key, algorithm=Settings.algorithm)
    return encoded_jwt
