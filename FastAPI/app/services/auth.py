from datetime import datetime, timedelta

from jose import JWTError, jwt

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.core.db import DbSessionDep
from app.core.exceptions import UnauthorizedError
from app.core.security import TokenDep, verify_password
from app.models.user import User


def authenticate_user(email: str, password: str, db: DbSessionDep) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid credentials")
    return user


async def get_current_user(token: TokenDep, db: DbSessionDep):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise UnauthorizedError("Token payload missing")
        user = db.query(User).filter(User.id == user_id).first()
        return user
    except JWTError:
        raise UnauthorizedError("Invalid or expired token")


def create_access_token(username: str, user_id: int):
    expires = datetime.utcnow() + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": username, "id": user_id, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
