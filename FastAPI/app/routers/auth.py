from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.core.db import DbSessionDep
from app.schemas.auth import Token
from app.schemas.user import UserCreate
from app.services.auth import authenticate_user, create_access_token
from app.services.user import create_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=201)
def register(user: UserCreate, db: DbSessionDep):
    user = create_user(db, user)
    token = create_access_token(user.username, user.id)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", response_model=Token, status_code=200)
def login(db: DbSessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password, db)
    token = create_access_token(user.username, user.id)
    return {"access_token": token, "token_type": "bearer"}
