from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import get_hashed_password, verify_password
from app.models.fridge import Fridge
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.utils.crud import get_or_404, update_by_id


# Users


async def create_user(db: AsyncSession, data: UserCreate):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalars().first():
        raise ConflictError("Email already registered")
    result = await db.execute(select(User).where(User.username == data.username))
    if result.scalars().first():
        raise ConflictError("Username already registered")
    user_instance = User(
        username=data.username,
        hashed_password=get_hashed_password(data.password),
        email=data.email,
    )
    db.add(user_instance)
    await db.flush()

    fridge_instance = Fridge(user_id=user_instance.id)
    db.add(fridge_instance)
    await db.commit()
    await db.refresh(user_instance)
    return user_instance


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate):
    return await update_by_id(db, User, user_id, data.model_dump(exclude_unset=True ))

async def change_user_email(db: AsyncSession, user_id: int, data: UserUpdateEmail):
    user = await get_or_404(db, User, user_id)

    try:
        user.email = data.new_email
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError("Email already registered")
    await db.refresh(user)
    return user

async def change_user_password(db: AsyncSession, user_id: int, data: UserUpdatePassword):
    user = await get_or_404(db, User, user_id)
    if not verify_password(data.old_password, user.hashed_password):
        raise ConflictError("Old password is incorrect")
    user.hashed_password = get_hashed_password(data.password)
    await db.commit()
    await db.refresh(user)
    return user