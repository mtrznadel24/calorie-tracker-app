import pytest

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import verify_password
from app.measurements.models import Weight
from app.user.models import Gender
from app.user.schemas import UserCreate, UserUpdate, UserUpdateEmail, UserUpdatePassword


@pytest.mark.integration
class TestUserService:
    async def test_create_user_success(self, user_service):
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
        result = await user_service.create_user(data)

        assert result.username == "testuser4"
        assert verify_password("Xfdk534@#", result.hashed_password)
        assert result.email == "testuser@gmail.com"
        assert result.gender == Gender.MALE
        assert result.fridge is not None

    async def test_create_user_username_already_exists(self, user_service, user):
        data = UserCreate(
            username="testuser",
            password="Xfdk534@#",
            confirm_password="Xfdk534@#",
            email="testuser@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )

        with pytest.raises(ConflictError):
            await user_service.create_user(data)

    async def test_create_user_email_already_exists(self, user_service, user):
        data = UserCreate(
            username="testuser4",
            password="Xfdk534@#",
            confirm_password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )

        with pytest.raises(ConflictError):
            await user_service.create_user(data)

    async def test_update_user_success(self, user_service, user):
        data = UserUpdate(username="testuserchanged", age=25)
        result = await user_service.update_user(user.id, data)

        assert result.username == "testuserchanged"
        assert result.age == 25

    async def test_get_user_username_already_exists(
        self, user_service, user, other_user
    ):
        data = UserUpdate(username="testuser2")

        with pytest.raises(ConflictError):
            await user_service.update_user(user.id, data)

    async def test_change_user_email_success(self, user_service, user):
        data = UserUpdateEmail(
            new_email="test_user_new@example.com",
            repeat_email="test_user_new@example.com",
        )

        result = await user_service.change_user_email(user.id, data)

        assert result.email == "test_user_new@example.com"

    async def test_change_user_email_email_already_exists(
        self, user_service, user, other_user
    ):
        data = UserUpdateEmail(
            new_email="test2@example.com", repeat_email="test2@example.com"
        )

        with pytest.raises(ConflictError):
            await user_service.change_user_email(user.id, data)

    async def test_change_user_password_success(self, user_service, user):
        data = UserUpdatePassword(
            old_password="password1",
            new_password="@GSS42d!dsa",
            repeat_password="@GSS42d!dsa",
        )

        result = await user_service.change_user_password(user.id, data)

        assert verify_password("@GSS42d!dsa", result.hashed_password)

    async def test_change_user_password_wrong_old_password(self, user_service, user):
        data = UserUpdatePassword(
            old_password="wrong_password",
            new_password="@GSS42d!dsa",
            repeat_password="@GSS42d!dsa",
        )

        with pytest.raises(UnauthorizedError):
            await user_service.change_user_password(user.id, data)

    async def test_get_user_bmr(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )
        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        result = await user_service.get_user_bmr(example_user)

        assert result == 1755

    async def test_get_user_bmr_lack_of_data(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            gender=Gender.MALE,
            activity_level=1.5,
        )
        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        with pytest.raises(ConflictError):
            await user_service.get_user_bmr(example_user)

    async def test_get_user_bmr_no_weight(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )

        with pytest.raises(ConflictError):
            await user_service.get_user_bmr(example_user)

    async def test_get_user_tdee_success(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
            activity_level=1.5,
        )

        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        result = await user_service.get_user_tdee(example_user)

        assert result == 2632

    async def test_get_user_tdee_no_activity_level(
        self, session, user_service, user_factory
    ):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
        )

        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        with pytest.raises(ConflictError):
            await user_service.get_user_tdee(example_user)

    async def test_get_user_bmi_success(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
        )

        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        result = await user_service.get_user_bmi(example_user)

        assert result == 23.1

    async def test_get_user_bmi_no_weight(self, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            height=180,
            age=25,
            gender=Gender.MALE,
        )

        with pytest.raises(ConflictError):
            await user_service.get_user_bmi(example_user)

    async def test_get_user_bmi_no_height(self, session, user_service, user_factory):
        example_user = await user_factory(
            username="testuser4",
            password="Xfdk534@#",
            email="test@example.com",
            age=25,
            gender=Gender.MALE,
        )

        weight = Weight(user_id=example_user.id, weight=75)
        session.add(weight)
        await session.commit()
        await session.refresh(weight)

        with pytest.raises(ConflictError):
            await user_service.get_user_bmi(example_user)
