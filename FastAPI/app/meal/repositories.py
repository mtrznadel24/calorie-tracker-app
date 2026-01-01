from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.base_repository import UserScopedRepository
from app.meal.models import MealLog


class MealRepository(UserScopedRepository[MealLog]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, MealLog)

    async def get_meal_logs(self, user_id: int, meal_date: date):
        stmt = select(MealLog).where(
            MealLog.user_id == user_id, MealLog.date == meal_date
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
