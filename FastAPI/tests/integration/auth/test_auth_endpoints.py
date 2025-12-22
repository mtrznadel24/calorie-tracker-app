import pytest


@pytest.mark.integration
class TestAuthEndpoints:
    # --- POST /auth/register ---

    async def test_register_success(self, client_with_redis):
        payload = {
            "username": "testuser43",
            "password": "F^9dHSA8*2f@",
            "confirm_password": "F^9dHSA8*2f@",
            "email": "testuser24@example.com",
            "height": 180,
            "age": 32,
            "gender": "male",
        }
        response = await client_with_redis.post("/auth/register", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert data["access_token"] is not None
        assert data["refresh_token"] is not None
        assert data["token_type"] == "bearer"

    async def test_register_weak_password(self, client_with_redis):
        payload = {
            "username": "testuser43",
            "password": "12345678",
            "confirm_password": "12345678",
            "email": "testuser24@example.com",
            "height": 180,
            "age": 32,
            "gender": "male",
        }
        response = await client_with_redis.post("/auth/register", json=payload)
        assert response.status_code == 422

    async def test_register_passwords_not_match(self, client_with_redis):
        payload = {
            "username": "testuser43",
            "password": "F^9dHSA8*2f@",
            "confirm_password": "F^9dHSA*2f@",
            "email": "testuser24@example.com",
            "height": 180,
            "age": 32,
            "gender": "male",
        }
        response = await client_with_redis.post("/auth/register", json=payload)
        assert response.status_code == 422

    async def test_register_wrong_data(self, client_with_redis):
        payload = {
            "username": "te",
            "password": "12345678",
            "confirm_password": "12345678",
            "email": "testuser24@example.com",
            "height": 180,
            "age": 32,
            "gender": "male",
        }
        response = await client_with_redis.post("/auth/register", json=payload)
        assert response.status_code == 422

    # --- POST /auth/login ---

    async def test_login_success(self, client_with_redis, user):
        payload = {"username": "test@example.com", "password": "password1"}
        response = await client_with_redis.post("/auth/login", data=payload)
        assert response.status_code == 200

        data = response.json()
        assert data["access_token"] is not None
        assert data["refresh_token"] is not None
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client_with_redis, user):
        payload = {"username": "test@example.com", "password": "password11"}
        response = await client_with_redis.post("/auth/login", data=payload)
        assert response.status_code == 401

    async def test_refresh_success(
        self, client_with_refresh_token, user, test_refresh_token
    ):
        response = await client_with_refresh_token.post(
            "/auth/refresh", json={"refresh_token": test_refresh_token}
        )
        assert response.status_code == 200

        data = response.json()
        assert data["access_token"] is not None
        assert data["refresh_token"] is not None
        assert data["refresh_token"] != test_refresh_token
        assert data["token_type"] == "bearer"

    async def test_logout_success(
        self, client_with_refresh_token, user, test_refresh_token
    ):
        response = await client_with_refresh_token.post(
            "/auth/logout", json={"refresh_token": test_refresh_token}
        )
        assert response.status_code == 200
