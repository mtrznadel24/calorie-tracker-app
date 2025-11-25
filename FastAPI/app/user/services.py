from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import get_hashed_password, verify_password
from app.fridge.models import Fridge
from app.measurements.repositories import WeightRepository
from app.user.models import User
from app.user.repositories import UserRepository
from app.user.schemas import UserCreate, UserUpdate, UserUpdateEmail, UserUpdatePassword
from app.utils.health_metrics import calculate_bmi, calculate_bmr, calculate_tdee

# Users


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
        self.weight_repo = WeightRepository(db)

    async def create_user(self, data: UserCreate) -> User:
        if await self.repo.get_user_by_email(data.email):
            raise ConflictError("Email already registered")
        if await self.repo.get_user_by_username(data.username):
            raise ConflictError("Username already registered")
        user_instance = User(
            **data.model_dump(exclude={"password", "confirm_password"}),
            hashed_password=get_hashed_password(data.password),
        )

        self.repo.add(user_instance)
        await self.repo.flush()

        fridge_instance = Fridge(user_id=user_instance.id)
        self.repo.add(fridge_instance)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("User already exists")
        return await self.repo.refresh_and_return(user_instance)

    async def update_user(self, user_id: int, data: UserUpdate) -> User:
        user_instance = await self.repo.get_by_id(user_id)

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user_instance, field, value)

        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("User already exists")
        return await self.repo.refresh_and_return(user_instance)

    async def change_user_email(self, user_id: int, data: UserUpdateEmail) -> User:
        user = await self.repo.get_by_id(user_id)
        user.email = data.new_email
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise ConflictError("Email already registered")
        return await self.repo.refresh_and_return(user)

    async def change_user_password(
        self, user_id: int, data: UserUpdatePassword
    ) -> User:
        user = await self.repo.get_by_id(user_id)
        if not verify_password(data.old_password, user.hashed_password):
            raise UnauthorizedError("Old password is incorrect")
        user.hashed_password = get_hashed_password(data.new_password)
        try:
            await self.repo.commit_or_conflict()
        except IntegrityError:
            raise UnauthorizedError("Password update failed")
        return await self.repo.refresh_and_return(user)

    async def get_user_bmr(self, user) -> int:
        if not all([user.height, user.age, user.gender]):
            raise ConflictError("Lack of user data")
        weight_in = await self.weight_repo.get_current_weight(user.id)
        if not weight_in:
            raise ConflictError("No weight data")
        weight = weight_in.weight
        try:
            return calculate_bmr(weight, user.height, user.age, user.gender)
        except ValueError:
            raise ConflictError("No weight data")  # Conflict error ?

    async def get_user_tdee(self, user) -> int:
        if not user.activity_level:
            raise ConflictError("No activity level")
        bmr = await self.get_user_bmr(user)
        return calculate_tdee(bmr, user.activity_level)

    async def get_user_bmi(self, user) -> float:
        if not user.height:
            raise ConflictError("No height data")
        height = user.height
        weight_obj = await self.weight_repo.get_current_weight(user.id)
        if not weight_obj:
            raise ConflictError("No weight data")
        weight = weight_obj.weight
        return calculate_bmi(weight, height)
