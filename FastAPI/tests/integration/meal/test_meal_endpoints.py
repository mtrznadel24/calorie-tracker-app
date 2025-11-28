import pytest

from app.meal.models import MealType
from tests.integration.meal.conftest import create_meals_with_ingredients


@pytest.mark.integration
class TestMealEndpoints:

    # --- POST /meals ---

    async def test_add_meal_success(self, client):
        payload = {
            "date": "2022-01-01",
            "type": "breakfast"
        }
        response = await client.post("/meals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    async def test_add_meal_no_auth(self, client_no_user):
        payload = {
            "date": "2022-01-01",
            "type": "breakfast"
        }
        response = await client_no_user.post("/meals", json=payload)
        assert response.status_code == 401

    async def test_add_meal_wrong_data(self, client):
        payload = {
            "date": "2022-01-01",
            "type": "breakfastsd"
        }
        response = await client.post("/meals", json=payload)
        assert response.status_code == 422

    async def test_add_meal_wrong_already_exists(self, client, sample_meal):
        payload = {
            "date": "2022-01-01",
            "type": "breakfast"
        }
        response = await client.post("/meals", json=payload)
        assert response.status_code == 409

    # --- GET /meals/lookup ---

    async def test_read_meal_success(self, client, sample_meal):
        payload = {
            "meal_date": "2022-01-01",
            "meal_type": "breakfast"
        }
        response = await client.get("/meals/lookup", params=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == "2022-01-01"
        assert data["type"] == "breakfast"

    async def test_read_meal_no_auth(self, client_no_user, sample_meal):
        payload = {
            "meal_date": "2022-01-01",
            "meal_type": "breakfast"
        }
        response = await client_no_user.get("/meals/lookup", params=payload)
        assert response.status_code == 401

    async def test_read_meal_no_meal(self, client):
        payload = {
            "meal_date": "2022-01-01",
            "meal_type": "breakfast"
        }
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

    async def test_get_meal_nutrient_sum_success(self, client, sample_meal_with_ingredients):
        response = await client.get(f"meals/{sample_meal_with_ingredients.id}/nutrients", params={"nutrient_type": "calories"})
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0.5*89 + 110 + 0.5*100

    async def test_get_meal_nutrient_sum_no_ingredient(self, client, sample_meal):
        response = await client.get(f"meals/{sample_meal.id}/nutrients", params={"nutrient_type": "calories"})
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0

    async def test_get_meal_nutrient_sum_no_auth(self, client_no_user, sample_meal_with_ingredients):
        response = await client_no_user.get(
            f"/meals/{sample_meal_with_ingredients.id}/nutrients",
            params={"nutrient_type": "calories"}
        )
        assert response.status_code == 401

    async def test_get_meal_nutrient_sum_wrong_meal_id(self, client):
        response = await client.get("/meals/99999/nutrients", params={"nutrient_type": "calories"})
        assert response.status_code == 404

    async def test_get_meal_nutrient_sum_invalid_param(self, client, sample_meal_with_ingredients):
        response = await client.get(
            f"/meals/{sample_meal_with_ingredients.id}/nutrients",
            params={"nutrient_type": "vitaminC"}
        )
        assert response.status_code == 422

    # --- GET /meals/{meal_id/macro

    async def test_get_meal_macro_success(self, client, sample_meal_with_ingredients):
        response = await client.get(f"meals/{sample_meal_with_ingredients.id}/macro")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert round(data["calories"], 1) == 204.5
        assert round(data["proteins"], 1) == 22.0
        assert round(data["fats"], 2) == 8.15
        assert round(data["carbs"], 1) == 69.6

    async def test_get_meal_macro_no_ingredients(self, client, sample_meal):
        response = await client.get(f"meals/{sample_meal.id}/macro")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert round(data["calories"], 1) == 0
        assert round(data["proteins"], 1) == 0
        assert round(data["fats"], 2) == 0
        assert round(data["carbs"], 1) == 0

    async def test_get_meal_macro_no_auth(self, client_no_user, sample_meal_with_ingredients):
        response = await client_no_user.get(f"/meals/{sample_meal_with_ingredients.id}/macro")
        assert response.status_code == 401

    async def test_get_meal_macro_wrong_meal_id(self, client):
        response = await client.get("/meals/99999/macro")
        assert response.status_code == 404

    async def test_get_meals_nutrient_sum_for_day_success(self, client, meal_factory, ingredient_factory):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        payload = {
            "meal_date": "2022-01-01",
            "nutrient_type": "calories"
        }
        response = await client.get(f"/meals/daily/nutrients", params=payload)
        print(response.json())
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 1477.5

    async def test_get_meals_nutrient_sum_for_day_no_auth(self, client_no_user, meal_factory, ingredient_factory):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        payload = {
            "meal_date": "2022-01-01",
            "nutrient_type": "calories"
        }
        response = await client_no_user.get(f"/meals/daily/nutrients", params=payload)
        assert response.status_code == 401


    async def test_get_meals_nutrient_sum_for_day_no_meals(self, client):
        payload = {
            "meal_date": "2022-01-01",
            "nutrient_type": "calories"
        }
        response = await client.get(f"/meals/daily/nutrients", params=payload)
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0


    async def test_get_macro_for_day_success(self, client, meal_factory, ingredient_factory):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        response = await client.get(f"/meals/daily/macro", params={"meal_date": "2022-01-01"})
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        expected = {
                    "calories": 1477.5,
                    "proteins": 121.7,
                    "fats": 17.7,
                    "carbs": 203.2
                   }
        assert data == expected

    async def test_get_macro_for_day_no_auth(self, client_no_user, meal_factory, ingredient_factory):
        await create_meals_with_ingredients(meal_factory, ingredient_factory)
        response = await client_no_user.get(f"/meals/daily/macro", params={"meal_date": "2022-01-01"})
        assert response.status_code == 401

    async def test_get_macro_for_day_no_meals(self, client):
        response = await client.get(f"/meals/daily/macro", params={"meal_date": "2022-01-01"})
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert data == {"calories": 0, "proteins": 0, "fats": 0, "carbs": 0}

