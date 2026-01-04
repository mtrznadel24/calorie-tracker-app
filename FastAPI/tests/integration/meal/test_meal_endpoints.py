import pytest

from app.fridge.models import FoodCategory
from app.meal.models import MealType


@pytest.mark.integration
class TestMealEndpoints:
    # --- POST /meals/quick ---
    async def test_quick_add_meal_log_success(self, client):
        payload = {
            "date": "2022-01-01",
            "type": "breakfast",
            "weight": 50,
            "name": "log1",
            "calories": 150,
            "proteins": 20,
            "fats": 15,
            "carbs": 30,
        }
        response = await client.post("/meals/quick", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["weight"] == 50
        assert data["calories"] == 150

    async def test_add_meal_log_wrong_data(self, client):
        payload = {
            "date": "2022-01-01",
            "type": "breakfastds",
            "weight": 50,
            "name": "log1",
            "calories": 150,
            "proteins": 20,
            "fats": 15,
            "carbs": 30,
        }
        response = await client.post("/meals/quick", json=payload)
        assert response.status_code == 422

    # --- POST /meals/from-product ---

    async def test_add_meal_log_from_fridge_product_success(
        self, client_with_fridge, fridge_product_factory
    ):
        product = await fridge_product_factory(
            product_name="Test Product",
            calories_100g=100,
            proteins_100g=10,
            fats_100g=10,
            carbs_100g=10,
            category=FoodCategory.DAIRY,
            is_favourite=False,
        )

        payload = {
            "fridge_product_id": product.id,
            "date": "2022-01-01",
            "type": "lunch",
            "weight": 50.0,  # Połowa porcji
        }

        response = await client_with_fridge.post("/meals/from-product", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert data["name"] == "Test Product"
        assert data["weight"] == 50.0
        assert data["calories"] == 50.0
        assert data["proteins"] == 5.0

    async def test_add_meal_log_from_fridge_product_not_found(self, client_with_fridge):
        payload = {
            "fridge_product_id": 9999,
            "date": "2022-01-01",
            "type": "lunch",
            "weight": 50.0,
        }
        response = await client_with_fridge.post("/meals/from-product", json=payload)
        assert response.status_code == 404

    # --- GET /meals/{log_id} ---

    async def test_read_meal_by_id_success(self, client, sample_meal_log):
        response = await client.get(f"/meals/{sample_meal_log.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_meal_log.id

    async def test_read_meal_by_id_not_found(self, client):
        response = await client.get("/meals/99999")
        assert response.status_code == 404

    # --- GET /meals/{date}/meal-logs ---

    async def test_read_meal_logs_by_date(self, client, meal_log_factory):
        await meal_log_factory(
            weight=100,
            type="breakfast",
            name="meal1",
            calories=100,
            proteins=10,
            fats=10,
            carbs=10,
        )
        await meal_log_factory(
            weight=100,
            type="dinner",
            name="meal2",
            calories=100,
            proteins=10,
            fats=10,
            carbs=10,
        )

        response = await client.get("/meals/2022-01-01/meal-logs")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        response_empty = await client.get("/meals/2022-01-02/meal-logs")
        assert response_empty.status_code == 200
        assert len(response_empty.json()) == 0

    # --- DELETE /meals/{log_id} ---

    async def test_delete_meal_log_success(self, client, sample_meal_log):
        response = await client.delete(f"/meals/{sample_meal_log.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_meal_log.id

        get_response = await client.get(f"/meals/{sample_meal_log.id}")
        assert get_response.status_code == 404

    async def test_delete_meal_log_not_found(self, client):
        response = await client.delete("/meals/99999")
        assert response.status_code == 404

        # --- POST /meals/from-meal ---

    async def test_add_meal_log_from_fridge_meal_success(
        self,
        client_with_fridge,
        fridge_meal_factory,
        fridge_product_factory,
        fridge_meal_ingredient_factory,
    ):
        prod1 = await fridge_product_factory(
            product_name="Egg",
            calories_100g=150,
            proteins_100g=10,
            fats_100g=10,
            carbs_100g=10,
            category=FoodCategory.DAIRY,
            is_favourite=False,
        )
        prod2 = await fridge_product_factory(
            product_name="Bacon",
            calories_100g=500,
            proteins_100g=10,
            fats_100g=10,
            carbs_100g=10,
            category=FoodCategory.DAIRY,
            is_favourite=False,
        )

        meal = await fridge_meal_factory("Scrambled Eggs")
        await fridge_meal_ingredient_factory(meal=meal, weight=100, product=prod1)
        await fridge_meal_ingredient_factory(meal=meal, weight=50, product=prod2)

        payload = {
            "fridge_meal_id": meal.id,
            "date": "2022-01-01",
            "type": "breakfast",
            "weight": 300.0,
        }

        response = await client_with_fridge.post("/meals/from-meal", json=payload)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2

        egg_log = next(d for d in data if d["name"] == "Egg")
        assert egg_log["weight"] == 200.0
        assert egg_log["calories"] == 300.0

        bacon_log = next(d for d in data if d["name"] == "Bacon")
        assert bacon_log["weight"] == 100.0
        assert bacon_log["calories"] == 500.0

    # --- PUT /meals/{log_id}/name ---

    async def test_update_meal_log_name_success(self, client, sample_meal_log):
        new_name = "Updated Name"
        response = await client.put(
            f"/meals/{sample_meal_log.id}/name", params={"log_name": new_name}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == new_name
        assert data["id"] == sample_meal_log.id

    # --- PUT /meals/{log_id}/weight ---

    async def test_update_meal_log_weight_recalculates_macros(
        self, client, meal_log_factory
    ):
        log = await meal_log_factory(
            type=MealType.BREAKFAST,
            name="meal_log",
            weight=100,
            calories=100,
            proteins=10,
            fats=10,
            carbs=10,
        )

        new_weight = 200
        response = await client.put(
            f"/meals/{log.id}/weight", params={"weight": new_weight}
        )

        assert response.status_code == 200
        data = response.json()

        assert data["weight"] == 200.0
        assert data["calories"] == 200.0
        assert data["proteins"] == 20.0
