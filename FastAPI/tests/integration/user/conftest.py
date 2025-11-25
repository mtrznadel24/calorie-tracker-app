import pytest_asyncio
from pydantic import EmailStr

from app.core.security import get_hashed_password
from app.user.models import Gender, User
from app.user.repositories import UserRepository
from app.user.services import UserService


@pytest_asyncio.fixture
def user_repo(session):
    return UserRepository(session)


@pytest_asyncio.fixture
def user_service(session):
    return UserService(session)


@pytest_asyncio.fixture
def user_factory(session):
    async def factory(
        username: str,
        password: str,
        email: EmailStr,
        height: float = None,
        age: int = None,
        gender: Gender = None,
        activity_level: float = None,
    ):
        hashed_password = get_hashed_password(password)
        u = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            height=height,
            age=age,
            gender=gender,
            activity_level=activity_level,
        )
        session.add(u)
        await session.commit()
        await session.refresh(u)
        return u

    return factory
