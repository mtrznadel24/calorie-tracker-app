from app.models import *
from sqlalchemy.orm import Session
from app.schemas.user import *

#Users

def create_user(db: Session, data: UserCreate):
    # TODO: Add password hashing
    user_instance = User(**data.model_dump())
    db.add(user_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance
