from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError
from app.core.security import get_hashed_password
from app.models.fridge import Fridge
from app.models.user import User
from app.schemas.user import UserCreate

# Users


def create_user(db: Session, data: UserCreate):
    if db.query(User).filter_by(email=data.email).first():
        raise ConflictError("Email already registered")
    if db.query(User).filter_by(username=data.username).first():
        raise ConflictError("Username already registered")
    user_instance = User(
        username=data.username,
        hashed_password=get_hashed_password(data.password),
        email=data.email,
    )
    db.add(user_instance)
    db.flush()

    fridge_instance = Fridge(user_id=user_instance.id)
    db.add(fridge_instance)
    db.commit()
    db.refresh(user_instance)
    return user_instance
