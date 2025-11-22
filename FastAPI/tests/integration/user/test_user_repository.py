import pytest
from sqlalchemy.exc import IntegrityError

from app.user.repositories import UserRepository


@pytest.mark.integration
class TestUserRepository:

    async def test_get_user_by_email(self, session, user):
        repo = UserRepository(session)

        result = await repo.get_user_by_email(user.email)

        assert result == user

    async def test_get_user_by_email_wrong_email(self, session, user):
        repo = UserRepository(session)

        result = await repo.get_user_by_email("wrong_email@gmail.com")

        assert result is None

    async def test_get_user_by_username(self, session, user):
        repo = UserRepository(session)

        result = await repo.get_user_by_username(user.username)

        assert result == user

    async def test_get_user_by_username_wrong_username(self, session, user):
        repo = UserRepository(session)

        result = await repo.get_user_by_username("wrong_username")

        assert result is None
