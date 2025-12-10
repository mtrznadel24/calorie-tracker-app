import pytest


@pytest.mark.integration
class TestRateLimiting:
    async def test_login_rate_limiting_per_username(
        self, client_with_redis, user, fake_redis
    ):
        payload = {"username": user.email, "password": "wrong_password"}
        for i in range(5):
            response = await client_with_redis.post("/auth/login", data=payload)
            assert response.status_code == 401
            assert await fake_redis.get(f"login_attempt:{user.email}") == str(i + 1)

        response = await client_with_redis.post("/auth/login", data=payload)
        assert response.status_code == 429

    async def test_successful_login_clears_counter(
        self, client_with_redis, user, fake_redis
    ):
        for i in range(4):
            response = await client_with_redis.post(
                "/auth/login",
                data={"username": user.email, "password": "wrong_password"},
            )
            assert response.status_code == 401
            assert await fake_redis.get(f"login_attempt:{user.email}") == str(i + 1)

        response = await client_with_redis.post(
            "/auth/login", data={"username": user.email, "password": "password1"}
        )
        assert response.status_code == 200

        assert await fake_redis.get(f"login_attempt:{user.email}") is None

        response = await client_with_redis.post(
            "/auth/login", data={"username": user.email, "password": "wrong_password"}
        )
        assert response.status_code == 401
