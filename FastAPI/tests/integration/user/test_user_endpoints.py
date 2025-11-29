import pytest


@pytest.mark.integration
class TestUserEndpoints:

    # --- GET /user/me ---

    async def test_read_current_user_success(self, client, user):
        response = await client.get("/user/me")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user.id
        assert data["username"] == user.username
        assert data["email"] == user.email

    async def test_read_current_user_no_auth(self, client_no_user):
        response = await client_no_user.get("/user/me")
        assert response.status_code == 401

    # --- PUT /user/me ---

    async def test_update_user_profile_success(self, client, user):

        response = await client.put("/user/me", json={"username": "updatetestuser"})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updatetestuser"

    async def test_update_user_profile_wrong_data(self, client, user):
        response = await client.put("/user/me", json={"username": "us"})
        assert response.status_code == 422

    # --- PUT /user/me/email ---

    async def test_update_user_email_success(self, client, user):
        response = await client.put("/user/me/email", json={"new_email": "newemail@example.com", "repeat_email": "newemail@example.com"})
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newemail@example.com"

    async def test_update_user_email_emails_not_match(self, client, user):
        response = await client.put("/user/me/email", json={"new_email": "newemail@example.com", "repeat_email": "newemail12@example.com"})
        assert response.status_code == 422


    # --- PUT /user/me/password ---

    async def test_update_user_password_success(self, client, user):
        payload = {"old_password": "password1",
                   "new_password": "Hs%hg254^#4S",
                   "repeat_password": "Hs%hg254^#4S"}
        response = await client.put("/user/me/password", json=payload)
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"

    async def test_update_user_password_wrong_old_password(self, client, user):
        payload = {"old_password": "password12",
                   "new_password": "Hs%hg254^#4S",
                   "repeat_password": "Hs%hg254^#4S"}
        response = await client.put("/user/me/password", json=payload)
        print(response.json())
        assert response.status_code == 401

    async def test_update_user_password_weak_password(self, client, user):
        payload = {"old_password": "password1",
                   "new_password": "12345678",
                   "repeat_password": "12345678"}
        response = await client.put("/user/me/password", json=payload)
        print(response.json())
        assert response.status_code == 422