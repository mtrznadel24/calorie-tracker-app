from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import get_hashed_password, verify_password
from app.models.fridge import Fridge
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.utils.crud import get_or_404, update_by_id


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


def update_user(db: Session, user_id: int, data: UserUpdate):
    return update_by_id(db, User, user_id, data.model_dump())

def change_user_email(db: Session, user_id: int, data: UserUpdateEmail):
    user = get_or_404(db, User, user_id)

    try:
        user.email = data.new_email
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ConflictError("Email already registered")
    db.refresh(user)
    return user

def change_user_password(db: Session, user_id: int, data: UserUpdatePassword):
    user = get_or_404(db, User, user_id)
    if not verify_password(data.old_password, user.hashed_password):
        raise ConflictError("Old password is incorrect")
    user.hashed_password = get_hashed_password(data.password)
    db.commit()
    db.refresh(user)
    return user