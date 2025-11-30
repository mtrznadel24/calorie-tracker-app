from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
from zxcvbn import zxcvbn

from app.user.models import Gender


def validate_password_strength(password: str) -> str:
    result = zxcvbn(password)
    if result["score"] < 3:
        warning = result["feedback"]["warning"]
        suggestions = result["feedback"]["suggestions"]
        msg = "Password is too weak."
        if warning:
            msg += f"\nWarning: {warning} "
        if suggestions:
            msg += "\nSuggestions:\n-" + "\n- ".join(suggestions)
        raise ValueError(msg)
    return password


def validate_passwords_match(password: str, confirm_password: str) -> str:
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    return password


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_.]+$",
        description="Username must be 3-32 characters, only letters, numbers, "
        "underscores and dots",
    )
    password: str = Field(min_length=8, max_length=64)
    confirm_password: str = Field(exclude=True, min_length=8, max_length=64)
    email: EmailStr
    height: float | None = Field(default=None, gt=0, lt=300)
    age: int | None = Field(default=None, gt=0, lt=120)
    gender: Gender | None
    activity_level: float | None = Field(default=None, ge=1, le=5)

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str):
        return validate_password_strength(value)

    @model_validator(mode="after")
    def check_passwords_match(self):
        validate_passwords_match(self.password, self.confirm_password)
        return self


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    height: float | None
    age: int | None
    gender: Gender | None
    activity_level: float | None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: str | None = Field(
        min_length=3,
        max_length=32,
        pattern=r"^[a-zA-Z0-9_.]+$",
        description="Username must be 3-32 characters, only letters, numbers, "
        "underscores and dots",
    )
    height: float | None = Field(default=None, gt=0, lt=300)
    age: int | None = Field(default=None, gt=0, lt=120)
    gender: Gender | None = Field(default=None)
    activity_level: float | None = Field(default=None, ge=1, le=5)


class UserUpdateEmail(BaseModel):
    new_email: EmailStr
    repeat_email: EmailStr

    @model_validator(mode="after")
    def check_emails_match(self):
        if self.new_email != self.repeat_email:
            raise ValueError("Emails do not match.")
        return self


class UserUpdatePassword(BaseModel):
    old_password: str = Field(min_length=8, max_length=64)
    new_password: str = Field(min_length=8, max_length=64)
    repeat_password: str = Field(min_length=8, max_length=64)

    @field_validator("new_password")
    @classmethod
    def check_password_strength(cls, value: str):
        return validate_password_strength(value)

    @model_validator(mode="after")
    def check_passwords_match(self):
        validate_passwords_match(self.new_password, self.repeat_password)
        return self
