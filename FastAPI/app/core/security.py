import uuid
from datetime import UTC, datetime, timedelta
from typing import Annotated

import argon2
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedError

argon2_context = PasswordHasher(
    time_cost=3,
    memory_cost=65536,
    parallelism=4,
    hash_len=32,
    salt_len=16,
    type=argon2.low_level.Type.ID,
)


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
TokenDep = Annotated[str, Depends(oauth2_bearer)]


def get_hashed_password(password: str) -> str:
    return argon2_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        argon2_context.verify(hashed_password, password)
        return True
    except (VerifyMismatchError, VerificationError, InvalidHashError):
        return False


def create_access_token(username: str, user_id: int) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.now(UTC) + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(username: str, user_id: int) -> tuple[str, str]:
    expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    jti = str(uuid.uuid4())
    expires = datetime.now(UTC) + expires_delta
    payload = {"sub": username, "id": user_id, "exp": expires, "jti": jti}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token, jti


def get_token_payload(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise UnauthorizedError("Invalid or expired token") from None
