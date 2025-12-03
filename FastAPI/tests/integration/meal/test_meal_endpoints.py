from datetime import date

import pytest

from app.fridge.models import FoodCategory
from app.meal.models import MealType
from tests.integration.meal.conftest import create_meals_with_ingredients


@pytest.mark.integration
class TestMealEndpoints:
    # --- POST /meals ---

    async def test_add_meal_success(self, client):
        payload = {"date": "2022-01-01", "type": "breakfast"}
        response = await client.post("/meals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    async def test_add_meal_no_auth(self, client_no_user):
        payload = {"date": "2022-01-01", "type": "breakfast"}
        response = await client_no_user.post("/meals", json=payload)
        assert response.status_code == 401

    async def test_add_meal_wrong_data(self, client):
        payload = {"date": "2022-01-01", "type": "breakfastsd"}
        response = await client.post("/meals", json=payload)
        assert response.status_code == 422

    async def test_add_meal_already_exists(self, client, sample_meal):
        payload = {"date": "2022-01-01", "type": "breakfast"}
        response = await client.post("/meals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    # --- GET /meals/lookup ---

    async def test_read_meal_success(self, client, sample_meal):
        payload = {"meal_date": "2022-01-01", "meal_type": "breakfast"}
        response = await client.get("/meals/lookup", params=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    async def test_read_meal_no_auth(self, client_no_user, sample_meal):
        payload = {"meal_date": "2022-01-01", "meal_type": "breakfast"}
        response = await client_no_user.get("/meals/lookup", params=payload)
        assert response.status_code == 401

    async def test_read_meal_no_meal(self, client):
        payload = {"meal_date": "2022-01-01", "meal_type": "breakfast"}
        response = await client.get("/meals/lookup", params=payload)
        assert response.status_code == 200
        data = response.json()
        assert data is None

    # --- GET /meals/{meal_id} ---

    async def test_read_meal_by_id_success(self, client, sample_meal):
        response = await client.get(f"/meals/{sample_meal.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_meal.id
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    async def test_read_meal_by_id_no_auth(self, client_no_user, sample_meal):
        response = await client_no_user.get(f"/meals/{sample_meal.id}")
        assert response.status_code == 401

    async def test_read_meal_by_id_not_found(self, client):
        response = await client.get("/meals/99999")
        assert response.status_code == 404

    # --- DELETE /meals/{meal_id} ---

    async def test_delete_meal_success(self, client, sample_meal):
        response = await client.delete(f"/meals/{sample_meal.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_meal.id

        follow_up = await client.get(f"/meals/{sample_meal.id}")
        assert follow_up.status_code == 404

    async def test_delete_meal_no_auth(self, client_no_user, sample_meal):
        response = await client_no_user.delete(f"/meals/{sample_meal.id}")
        assert response.status_code == 401

    async def test_delete_meal_not_found(self, client):
        response = await client.delete("/meals/99999")
        assert response.status_code == 404

    # --- GET /meals/{meal_id}/nutrients

    async def test_get_meal_nutrient_sum_success(
        self, client, sample_meal_with_ingredients
    ):
        response = await client.get(
            f"meals/{sample_meal_with_ingredients.id}/nutrients",
            params={"nutrient_type": "calories"},
        )
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == round(0.5 * 89 + 110 + 0.5 * 100, 0)

    async def test_get_meal_nutrient_sum_no_ingredient(self, client, sample_meal):
        response = await client.get(
            f"meals/{sample_meal.id}/nutrients", params={"nutrient_type": "calories"}
        )
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0

    async def test_get_meal_nutrient_sum_no_auth(
        self, client_no_user, sample_meal_with_ingredients
    ):
        response = await client_no_user.get(
            f"/meals/{sample_meal_with_ingredients.id}/nutrients",
            params={"nutrient_type": "calories"},
        )
        assert response.status_code == 401

    async def test_get_meal_nutrient_sum_wrong_meal_id(self, client):
        response = await client.get(
            "/meals/99999/nutrients", params={"nutrient_type": "calories"}
        )
        assert response.status_code == 404

    async def test_get_meal_nutrient_sum_invalid_param(
        self, client, sample_meal_with_ingredients
    ):
        response = await client.get(
            f"/meals/{sample_meal_with_ingredients.id}/nutrients",
            params={"nutrient_type": "vitaminC"},
        )
        assert response.status_code == 422

    # --- GET /meals/{meal_id/macro

    async def test_get_meal_macro_success(self, client, sample_meal_with_ingredients):
        response = await client.get(f"meals/{sample_meal_with_ingredients.id}/macro")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["calories"] == round(204.5, 0)
        assert data["proteins"] == round(22.0, 1)
        assert data["fats"] == round(8.15, 1)
        assert data["carbs"] == round(69.6, 1)

    async def test_get_meal_macro_no_ingredients(self, client, sample_meal):
        response = await client.get(f"meals/{sample_meal.id}/macro")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data["calories"] == 0, 1
        assert data["proteins"] == 0
        assert data["fats"] == 0
        assert data["carbs"] == 0

    async def test_get_meal_macro_no_auth(
        self, client_no_user, sample_meal_with_ingredients
    ):
        response = await client_no_user.get(
            f"/meals/{sample_meal_with_ingredients.id}/macro"
        )
        assert response.status_code == 401

    async def test_get_meal_macro_wrong_meal_id(self, client):
        response = await client.get("/meals/99999/macro")
        assert response.status_code == 404

    async def test_get_meals_nutrient_sum_for_day_success(
        self, client, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        payload = {"meal_date": "2022-01-01", "nutrient_type": "calories"}
        response = await client.get("/meals/daily/nutrients", params=payload)
        print(response.json())
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == round(1477.5, 0)

    async def test_get_meals_nutrient_sum_for_day_no_auth(
        self, client_no_user, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        payload = {"meal_date": "2022-01-01", "nutrient_type": "calories"}
        response = await client_no_user.get("/meals/daily/nutrients", params=payload)
        assert response.status_code == 401

    async def test_get_meals_nutrient_sum_for_day_no_meals(self, client):
        payload = {"meal_date": "2022-01-01", "nutrient_type": "calories"}
        response = await client.get("/meals/daily/nutrients", params=payload)
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0

    async def test_get_macro_for_day_success(
        self, client, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        response = await client.get(
            "/meals/daily/macro", params={"meal_date": "2022-01-01"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        expected = {
            "calories": round(1477.5, 0),
            "proteins": 121.7,
            "fats": 17.7,
            "carbs": 203.2,
        }
        assert data == expected

    async def test_get_macro_for_day_no_auth(
        self, client_no_user, meal_factory, ingredient_factory
    ):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        response = await client_no_user.get(
            "/meals/daily/macro", params={"meal_date": "2022-01-01"}
        )
        assert response.status_code == 401

    async def test_get_macro_for_day_no_meals(self, client):
        response = await client.get(
            "/meals/daily/macro", params={"meal_date": "2022-01-01"}
        )
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data == {"calories": 0, "proteins": 0, "fats": 0, "carbs": 0}

    # POST /{meal_date}/{meal_type}/ingredients/from-fridge-product/{fridge_product_id}

    async def test_add_fridge_product_to_meal_success(
        self, client_with_fridge, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=25,
            fats_100g=10,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )
        payload = {"weight": 50}
        response = await client_with_fridge.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-product/{product.id}",
            json=payload,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["weight"] == 50
        assert isinstance(data["id"], int)
        details = data["details"]
        assert details["product_name"] == "Product1"
        assert details["calories_100g"] == 150

    async def test_add_fridge_product_to_meal_success_meal_exits(
        self, client_with_fridge, sample_meal, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=25,
            fats_100g=10,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )
        payload = {"weight": 50}
        response = await client_with_fridge.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-product/{product.id}",
            json=payload,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["weight"] == 50
        assert isinstance(data["id"], int)
        details = data["details"]
        assert details["product_name"] == "Product1"
        assert details["calories_100g"] == 150

        async def test_add_fridge_product_to_meal_success_meal_exits(
            self, client_with_fridge, sample_meal, fridge_product_factory
        ):
            product = await fridge_product_factory(
                product_name="Product1",
                calories_100g=150,
                proteins_100g=25,
                fats_100g=10,
                carbs_100g=40,
                category=FoodCategory.FRUIT,
                is_favourite=False,
            )
            payload = {"weight": 50}
            response = await client_with_fridge.post(
                f"/meals/{date(2022, 1, 1)}/"
                f"{MealType.BREAKFAST.value}/"
                f"ingredients/from-fridge-product/{product.id}",
                json=payload,
            )
            assert response.status_code == 200
            data = response.json()
            assert data["weight"] == 50
            assert isinstance(data["id"], int)
            details = data["details"]
            assert details["product_name"] == "Product1"
            assert details["calories_100g"] == 150

    async def test_add_fridge_product_to_meal_no_auth(
        self, client_no_user, sample_meal, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Product1",
            calories_100g=150,
            proteins_100g=25,
            fats_100g=10,
            carbs_100g=40,
            category=FoodCategory.FRUIT,
            is_favourite=False,
        )
        payload = {"weight": 50}
        response = await client_no_user.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-product/{product.id}",
            json=payload,
        )
        assert response.status_code == 401

    async def test_add_fridge_product_to_meal_wrong_product_id(
        self, client_with_fridge, sample_meal, fridge_product_factory
    ):
        payload = {"weight": 50}
        response = await client_with_fridge.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-product/99999",
            json=payload,
        )
        assert response.status_code == 404

    # - POST /{meal_date}/{meal_type}/ingredients/from-fridge-meal/{fridge_meal_id} -

    async def test_add_fridge_meal_to_meal_success(
        self,
        client_with_fridge,
        fridge_product_factory,
        fridge_meal_factory,
        fridge_meal_ingredient_factory,
    ):
        fridge_meal = await fridge_meal_factory(meal_name="Meal1")
        fridge_products = [
            await fridge_product_factory(
                product_name=name,
                calories_100g=150,
                proteins_100g=25,
                fats_100g=10,
                carbs_100g=40,
                category=FoodCategory.FRUIT,
                is_favourite=False,
            )
            for name in ["Product1", "Product2", "Product3"]
        ]
        [
            await fridge_meal_ingredient_factory(fridge_meal, 50, prod)
            for prod in fridge_products
        ]

        payload = {"weight": 50}
        response = await client_with_fridge.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-meal/{fridge_meal.id}",
            json=payload,
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        assert len(data) == 3

        for i, ingredient in enumerate(data):
            assert isinstance(ingredient["id"], int)
            assert ingredient["weight"] == 17.0

            details = ingredient["details"]
            assert details["product_name"] == f"Product{i + 1}"
            assert details["calories_100g"] == 150.0
            assert details["proteins_100g"] == 25.0
            assert details["fats_100g"] == 10.0
            assert details["carbs_100g"] == 40.0

    async def test_add_fridge_meal_to_meal_fridge_meal_no_ingredients(
        self,
        client_with_fridge,
        fridge_product_factory,
        fridge_meal_factory,
        fridge_meal_ingredient_factory,
    ):
        fridge_meal = await fridge_meal_factory(meal_name="Meal1")

        payload = {"weight": 50}
        response = await client_with_fridge.post(
            f"/meals/{date(2022, 1, 1)}/"
            f"{MealType.BREAKFAST.value}/"
            f"ingredients/from-fridge-meal/{fridge_meal.id}",
            json=payload,
        )
        assert response.status_code == 404
