from app.models import *
from sqlalchemy.orm import Session
from app.schemas.user import *
from app.auth import get_hashed_password


#Users

def create_user(db: Session, data: UserCreate):
    # TODO: Add creating fridge
    user_instance = User(
        username=data.username,
        hashed_password=get_hashed_password(data.password),
        email=data.email,

    )
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)

    return user_instance
