from typing import Annotated

import uuid
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt

from app.models.user import User
from app.services.auth import get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS ,ALGORITHM, SECRET_KEY

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
TokenDep = Annotated[str, Depends(oauth2_bearer)]

UserDep = Annotated[User, Depends(get_current_user)]


def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(password, hashed_password)


def create_access_token(username: str, user_id: int):
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.utcnow() + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(username: str, user_id: int):
    expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    expires = datetime.utcnow() + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires, "jti": jti}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token, jti