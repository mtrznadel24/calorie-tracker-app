import pytest
from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import UnauthorizedError
from app.core.security import create_refresh_token, get_token_payload
from app.user.models import Gender
from app.user.schemas import UserCreate


@pytest.mark.integration
class TestAuthService:

    async def test_authenticate_user_success(self, auth_service, user):
        result = await auth_service.authenticate_user("test@example.com", "password1")

        assert result.id == user.id
        assert result.username == user.username
        assert result.email == user.email

    async def test_authenticate_user_wrong_email(self, auth_service, user):
        with pytest.raises(UnauthorizedError):
            await auth_service.authenticate_user("test23@example.com", "password1")

    async def test_authenticate_user_wrong_password(self, auth_service, user):
        with pytest.raises(UnauthorizedError):
            await auth_service.authenticate_user("test@example.com", "password3")

    async def test_register_user_success(self, auth_service):
        data = UserCreate(
            username="testuser4",
            password="Xfdk534@#",
            confirm_password="Xfdk534@#",
            email="testuser@gmail.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )
        access_token, refresh_token = await auth_service.register_user(data)

        assert isinstance(access_token, str)
        assert isinstance(refresh_token, str)
        assert access_token != ""
        assert refresh_token != ""

        access_payload = get_token_payload(access_token)
        assert access_payload["sub"] == "testuser4"

    async def test_login_user_success(self, auth_service, user):
        form_data = OAuth2PasswordRequestForm(
            username="test@example.com", password="password1", scope=""
        )
        access_token, refresh_token = await auth_service.login_user(form_data)

        assert isinstance(access_token, str)
        assert isinstance(refresh_token, str)
        assert access_token != ""
        assert refresh_token != ""

        access_payload = get_token_payload(access_token)
        assert access_payload["sub"] == "testuser"

    async def test_refresh_tokens_success(self, auth_service, token_repo, user):
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await token_repo.add_refresh_token_to_redis(jti, user.id)
        access_token, new_refresh_token = await auth_service.refresh_tokens(
            refresh_token
        )

        assert not await token_repo.is_refresh_token_valid(jti)

        assert isinstance(access_token, str)
        assert isinstance(refresh_token, str)
        assert access_token != ""
        assert refresh_token != ""

        refresh_payload = get_token_payload(new_refresh_token)
        new_jti = refresh_payload["jti"]
        assert await token_repo.is_refresh_token_valid(new_jti)

        access_payload = get_token_payload(access_token)
        assert access_payload["sub"] == "testuser"

    async def test_refresh_tokens_refresh_token_not_exist(
        self, auth_service, token_repo, user
    ):
        refresh_token, jti = create_refresh_token(user.username, user.id)

        with pytest.raises(UnauthorizedError):
            await auth_service.refresh_tokens(refresh_token)

        assert not await token_repo.is_refresh_token_valid(jti)

    async def test_logout_user_success(self, auth_service, token_repo, user):
        refresh_token, jti = create_refresh_token(user.username, user.id)
        await token_repo.add_refresh_token_to_redis(jti, user.id)
        await auth_service.logout_user(refresh_token)
        assert not await token_repo.is_refresh_token_valid(jti)
