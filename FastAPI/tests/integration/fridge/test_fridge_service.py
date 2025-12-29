import pytest

from app.core.exceptions import ConflictError, NotFoundError
from app.fridge.models import FoodCategory
from app.fridge.schemas import (
    FridgeMealIngredientCreate,
    FridgeMealIngredientUpdate,
    FridgeMealUpdate,
    FridgeMealWithIngredientsCreate,
    FridgeProductCreate,
    FridgeProductUpdate,
)


@pytest.mark.integration
class TestFridgeService:
    async def test_create_fridge_product_success(self, fridge_service, fridge):
        data = FridgeProductCreate(
            product_name="Product1",
            calories_100g=100,
            proteins_100g=50,
            fats_100g=15,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=True,
        )

        result = await fridge_service.create_fridge_product(fridge.id, data)

        assert result.product_name == "Product1"
        assert result.calories_100g == 100
        assert result.fridge_id == fridge.id

    async def test_create_fridge_product_conflict(
        self, fridge_service, fridge, sample_fridge_product
    ):
        data = FridgeProductCreate(
            product_name="Banana",
            calories_100g=100,
            proteins_100g=50,
            fats_100g=15,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=True,
        )

        with pytest.raises(ConflictError):
            await fridge_service.create_fridge_product(fridge.id, data)

    async def test_update_fridge_product_success(
        self, fridge_service, fridge, sample_fridge_product
    ):
        data = FridgeProductUpdate(product_name="Product1", calories_100g=280)

        result = await fridge_service.update_fridge_product(
            fridge.id, sample_fridge_product.id, data
        )

        assert result.product_name == "Product1"
        assert result.calories_100g == 280

    async def test_update_fridge_product_conflict(
        self, fridge_service, fridge, sample_fridge_product, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Product1",
            calories_100g=100,
            proteins_100g=50,
            fats_100g=15,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=True,
        )
        data = FridgeProductUpdate(product_name="Banana", calories_100g=280)

        with pytest.raises(ConflictError):
            await fridge_service.update_fridge_product(fridge.id, product.id, data)

    async def test_delete_fridge_product_success(
        self, fridge_service, fridge, sample_fridge_product
    ):
        result = await fridge_service.delete_fridge_product(
            fridge.id, sample_fridge_product.id
        )
        assert result.id == sample_fridge_product.id

    async def test_create_fridge_meal_success(self, fridge_service, fridge):
        data = FridgeMealWithIngredientsCreate(
            name="Pasta", is_favourite=True, ingredients=[]
        )

        result = await fridge_service.create_fridge_meal(fridge.id, data)

        assert result.name == "Pasta"
        assert result.is_favourite is True

    async def test_create_fridge_meal_conflict(
        self, fridge_service, fridge, sample_fridge_meal
    ):
        data = FridgeMealWithIngredientsCreate(
            name="toast", is_favourite=True, ingredients=[]
        )

        with pytest.raises(ConflictError):
            await fridge_service.create_fridge_meal(fridge.id, data)

    async def test_get_fridge_meals_success(
        self, fridge_service, fridge, fridge_meal_factory
    ):
        await fridge_meal_factory("Soup")
        await fridge_meal_factory("Salad")

        result = await fridge_service.get_fridge_meals(fridge.id)

        assert isinstance(result, list)
        assert any(meal.name == "Soup" for meal in result)
        assert any(meal.name == "Salad" for meal in result)

    async def test_get_fridge_meal_success(
        self, fridge_service, fridge, sample_fridge_meal
    ):
        result = await fridge_service.get_fridge_meal(fridge.id, sample_fridge_meal.id)

        assert result.id == sample_fridge_meal.id
        assert result.name == "toast"

    async def test_update_fridge_meal_success(
        self, fridge_service, fridge, sample_fridge_meal
    ):
        data = FridgeMealUpdate(name="UpdatedToast", is_favourite=True)

        result = await fridge_service.update_fridge_meal(
            fridge.id, sample_fridge_meal.id, data
        )

        assert result.name == "UpdatedToast"
        assert result.is_favourite is True

    async def test_update_fridge_meal_conflict(
        self, fridge_service, fridge, sample_fridge_meal, fridge_meal_factory
    ):
        other_meal = await fridge_meal_factory("Soup")
        data = FridgeMealUpdate(name="toast")

        with pytest.raises(ConflictError):
            await fridge_service.update_fridge_meal(fridge.id, other_meal.id, data)

    async def test_delete_fridge_meal_success(
        self, fridge_service, fridge, sample_fridge_meal
    ):
        result = await fridge_service.delete_fridge_meal(
            fridge.id, sample_fridge_meal.id
        )
        assert result.id == sample_fridge_meal.id

    async def test_add_fridge_meal_ingredient_success(
        self, fridge_service, fridge, sample_fridge_meal, sample_fridge_product
    ):
        data = FridgeMealIngredientCreate(
            weight=50, fridge_product_id=sample_fridge_product.id
        )

        result = await fridge_service.add_fridge_meal_ingredient(
            fridge.id, sample_fridge_meal.id, data
        )

        assert result.weight == 50
        assert result.fridge_product_id == sample_fridge_product.id

    async def test_update_fridge_meal_ingredient_success(
        self,
        fridge_service,
        fridge,
        sample_fridge_meal,
        fridge_meal_ingredient_factory,
        sample_fridge_product,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            meal=sample_fridge_meal, weight=30, product=sample_fridge_product
        )

        data = FridgeMealIngredientUpdate(weight=50)

        result = await fridge_service.update_fridge_meal_ingredient(
            fridge.id, sample_fridge_meal.id, ingredient.id, data
        )

        assert result.weight == 50
        assert result.fridge_product_id == sample_fridge_product.id

    async def test_delete_fridge_meal_ingredient_success(
        self,
        fridge_service,
        fridge,
        sample_fridge_meal,
        fridge_meal_ingredient_factory,
        sample_fridge_product,
    ):
        ingredient = await fridge_meal_ingredient_factory(
            meal=sample_fridge_meal, weight=10, product=sample_fridge_product
        )

        result = await fridge_service.delete_fridge_meal_ingredient(
            fridge.id, sample_fridge_meal.id, ingredient.id
        )

        assert result.id == ingredient.id

    async def test_delete_fridge_meal_ingredient_wrong_meal(
        self, fridge_service, fridge, sample_fridge_meal_with_ingredient
    ):
        ingredient = sample_fridge_meal_with_ingredient.ingredients[0]

        with pytest.raises(NotFoundError):
            await fridge_service.delete_fridge_meal_ingredient(
                fridge.id, 9999, ingredient.id
            )
