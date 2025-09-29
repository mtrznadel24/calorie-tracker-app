import os

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_hashed_password(password: str) -> str:
    return bcrypt_context.hash(password)