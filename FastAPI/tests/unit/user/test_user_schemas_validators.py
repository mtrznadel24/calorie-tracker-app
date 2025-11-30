import pytest

from app.user.schemas import (
    UserUpdateEmail,
    validate_password_strength,
    validate_passwords_match,
)


@pytest.mark.unit
class TestSchemasValidators:
    def test_validate_passwords_strength(self):
        password = "HF&6VJF7fas98*8"
        result = validate_password_strength(password)
        assert result == password

    def test_validate_passwords_strength_too_weak(self):
        password = "12345678"
        with pytest.raises(ValueError):
            validate_password_strength(password)

    def test_validate_passwords_match(self):
        password = "password1"
        confirm_password = "password1"
        result = validate_passwords_match(password, confirm_password)

        assert result == password

    def test_validate_passwords_match_not_match(self):
        password = "password1"
        confirm_password = "password12"
        with pytest.raises(ValueError):
            validate_passwords_match(password, confirm_password)

    def test_user_update_email_schema_success(self):
        data = UserUpdateEmail(
            new_email="testuser@example.com",
            repeat_email="testuser@example.com",
        )
        assert data.new_email == "testuser@example.com"

    def test_user_update_email_schema_not_match(self):
        with pytest.raises(ValueError):
            UserUpdateEmail(
                new_email="testuser@example.com",
                repeat_email="testuser2@example.com",
            )
