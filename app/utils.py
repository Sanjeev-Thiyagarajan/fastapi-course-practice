from . import schemas, config
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=config.settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, config.settings.secret_key, algorithms=[config.settings.algorithm])

        id: int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
        print(token_data)
    except JWTError:
        raise credentials_exception

    return token_data
