from sqlalchemy import select, desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError
from app.core.security import get_hashed_password, verify_password
from app.models.fridge import Fridge
from app.models.user import User, Weight
from app.schemas.user import UserCreate, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.services.measurements import get_current_weight
from app.utils.crud import get_or_404, update_by_id

# Users


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
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
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError("User already exists")
    await db.refresh(user_instance)
    return user_instance


async def update_user(db: AsyncSession, user_id: int, data: UserUpdate) -> User:
    return await update_by_id(db, User, user_id, data.model_dump(exclude_unset=True))


async def change_user_email(
    db: AsyncSession, user_id: int, data: UserUpdateEmail
) -> User:
    user = await get_or_404(db, User, user_id)

    try:
        user.email = data.new_email
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError("Email already registered")
    await db.refresh(user)
    return user


async def change_user_password(
    db: AsyncSession, user_id: int, data: UserUpdatePassword
) -> User:
    user = await get_or_404(db, User, user_id)
    if not verify_password(data.old_password, user.hashed_password):
        raise ConflictError("Old password is incorrect")
    user.hashed_password = get_hashed_password(data.password)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise ConflictError("Password update failed")
    return user


async def get_user_bmr(db: AsyncSession, user) -> int:
    if not all([user.height, user.age, user.gender, user.activity_level]):
        raise ConflictError("Lack of user data")
    weight_obj = await get_current_weight(db, user.user_id)
    if not weight_obj:
        raise ConflictError("No weight data")
    weight = weight_obj.weight
    if user.gender == "M":
        return int((10 * weight) + (6.25 * user.height) - (5 * user.age) + 5)
    elif user.gender == "F":
        return int((10 * weight) + (6.25 * user.height) - (5 * user.age) - 161)
    else:
        raise ConflictError("Unknown gender")

async def get_user_tdee(db: AsyncSession, user) -> int:
    BMR = await get_user_bmr(db, user)
    return BMR * user.activity_level

async def get_user_bmi(db: AsyncSession, user) -> float:
    if not user.height:
        raise ConflictError("No height data")
    height = user.height
    height /= 100
    weight_obj = await get_current_weight(db, user.user_id)
    if not weight_obj:
        raise ConflictError("No weight data")
    weight = weight_obj.weight
    return round((weight / height**2), 2)