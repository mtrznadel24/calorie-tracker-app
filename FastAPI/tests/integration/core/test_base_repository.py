import pytest

from app.core.exceptions import NotFoundError
from app.user.repositories import UserRepository


@pytest.mark.integration
class TestBaseRepository:

    async def test_get_by_id_success(self, session, user):
        repo = UserRepository(session)

        result = await repo.get_by_id(user.id)

        assert result == user

    async def test_get_by_id_not_found(self, session, user):
        repo = UserRepository(session)

        with pytest.raises(NotFoundError):
            await repo.get_by_id(999)

    async def test_delete_by_id_success(self, session, user):
        repo = UserRepository(session)
        result = await repo.delete_by_id(user.id)
        assert result == user

    async def test_delete_by_id_not_found(self, session, user):
        repo = UserRepository(session)
        with pytest.raises(NotFoundError):
            await repo.delete_by_id(999)