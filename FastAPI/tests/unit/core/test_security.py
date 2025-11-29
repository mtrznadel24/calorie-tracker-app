import uuid
from datetime import datetime, timezone, timedelta

import pytest
from jose import jwt

from app.core.config import settings
from app.core.exceptions import UnauthorizedError
from app.core.security import get_hashed_password, verify_password, create_access_token, get_token_payload, \
    create_refresh_token


@pytest.mark.unit
class TestSecurity:

    def test_verify_password_true(self):
        password = "password1"
        hashed_password = get_hashed_password(password)
        assert verify_password(password, hashed_password) == True

    def test_verify_password_false(self):
        password = "password1"
        hashed_password = get_hashed_password("password2")
        assert verify_password(password, hashed_password) == False

    def test_create_access_token_structure(self):
        token = create_access_token("testuser", 123)
        payload = get_token_payload(token)

        assert payload["sub"] == "testuser"
        assert payload["id"] == 123
        assert "exp" in payload

    def test_create_refresh_token_structure(self):
        token, jti = create_refresh_token("testuser", 123)
        payload = get_token_payload(token)

        assert payload["sub"] == "testuser"
        assert payload["id"] == 123
        assert payload["jti"] == jti
        assert "exp" in payload

    def test_create_refresh_token_jti_is_uuid(self):
        token, jti = create_refresh_token("testuser", 123)

        uuid.UUID(jti)
        assert len(jti) == 36

    def test_get_token_payload_invalid_token(self):
        with pytest.raises(UnauthorizedError, match="Invalid or expired token"):
            get_token_payload("invalid.token.here")

    def test_get_token_payload_expired_token(self):
        past = datetime.now(timezone.utc) - timedelta(hours=1)
        payload = {"sub": "test", "id": 1, "exp": past}
        expired_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        with pytest.raises(UnauthorizedError, match="Invalid or expired token"):
            get_token_payload(expired_token)