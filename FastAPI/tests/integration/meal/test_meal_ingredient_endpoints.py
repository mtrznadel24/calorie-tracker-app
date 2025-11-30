import pytest


@pytest.mark.integration
class TestMealIngredientEndpoints:
    # --- POST /meals/{meal_id}/ingredients

    async def test_add_ingredient_to_meal_success(self, client, sample_meal):
        payload = {
            "weight": 50,
            "details": {
                "product_name": "product1",
                "calories_100g": 160,
                "proteins_100g": 40,
                "fats_100g": 20,
                "carbs_100g": 60,
            },
        }
        response = await client.post(
            f"/meals/{sample_meal.id}/ingredients", json=payload
        )
        assert response.status_code == 200
        data = response.json()
        details = data["details"]
        assert isinstance(data["id"], int)
        assert data["weight"] == 50
        assert details["product_name"] == "product1"
        assert details["calories_100g"] == 160
        assert details["proteins_100g"] == 40
        assert details["fats_100g"] == 20
        assert details["carbs_100g"] == 60

    async def test_add_ingredient_to_meal_no_auth(self, client_no_user, sample_meal):
        payload = {
            "weight": 50,
            "details": {
                "product_name": "product1",
                "calories_100g": 160,
                "proteins_100g": 40,
                "fats_100g": 20,
                "carbs_100g": 60,
            },
        }
        response = await client_no_user.post(
            f"/meals/{sample_meal.id}/ingredients", json=payload
        )
        assert response.status_code == 401

    async def test_add_ingredient_to_meal_no_meal(self, client, sample_meal):
        payload = {
            "weight": 50,
            "details": {
                "product_name": "product1",
                "calories_100g": 160,
                "proteins_100g": 40,
                "fats_100g": 20,
                "carbs_100g": 60,
            },
        }
        response = await client.post("/meals/9999/ingredients", json=payload)
        assert response.status_code == 404

    async def test_add_ingredient_to_meal_wrong_data(self, client, sample_meal):
        payload = {
            "weight": -2,
            "details": {
                "product_name": "product1",
                "calories_100g": 160,
                "proteins_100g": 40,
                "fats_100g": 20,
                "carbs_100g": 60,
            },
        }
        response = await client.post(
            f"/meals/{sample_meal.id}/ingredients", json=payload
        )
        assert response.status_code == 422

    # --- GET /meals/{meal_id}/ingredients ---

    async def test_read_meal_ingredients_success(
        self, client, sample_meal_with_ingredients
    ):
        ingredients = sample_meal_with_ingredients.ingredients
        response = await client.get(
            f"/meals/{sample_meal_with_ingredients.id}/ingredients"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(ingredients)
        for idx, ingredient in enumerate(ingredients):
            assert data[idx]["id"] == ingredient.id

    async def test_read_meal_ingredients_no_auth(
        self, client_no_user, sample_meal_with_ingredients
    ):
        response = await client_no_user.get(
            f"/meals/{sample_meal_with_ingredients.id}/ingredients"
        )
        assert response.status_code == 401

    async def test_read_meal_ingredients_wrong_meal_id(self, client):
        response = await client.get("/meals/9999/ingredients")
        assert response.status_code == 404

    # --- GET /meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_read_meal_ingredient_success(
        self, client, sample_meal_with_ingredients
    ):
        ingredient = sample_meal_with_ingredients.ingredients[0]
        response = await client.get(
            f"/meals/{sample_meal_with_ingredients.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingredient.id

    async def test_read_meal_ingredient_no_auth(
        self, client_no_user, sample_meal_with_ingredients
    ):
        ingredient = sample_meal_with_ingredients.ingredients[0]
        response = await client_no_user.get(
            f"/meals/{sample_meal_with_ingredients.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 401

    async def test_read_meal_ingredient_wrong_ids(self, client):
        response = await client.get("/meals/9999/ingredients/9999")
        assert response.status_code == 404

    # --- PUT /meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_update_meal_ingredient_success(
        self, client, sample_meal_with_ingredient
    ):
        payload = {
            "weight": 100,
            "details": {
                "product_name": "product3",
                "proteins_100g": 20,
                "fats_100g": 15,
            },
        }
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client.put(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/{ingredient.id}",
            json=payload,
        )
        assert response.status_code == 200
        data = response.json()
        details = data["details"]
        assert isinstance(data["id"], int)
        assert data["weight"] == 100
        assert details["product_name"] == "product3"
        assert details["proteins_100g"] == 20
        assert details["fats_100g"] == 15
        assert details["carbs_100g"] == 23
        assert details["calories_100g"] == 89

    async def test_update_meal_ingredient_no_auth(
        self, client_no_user, sample_meal_with_ingredient
    ):
        payload = {
            "weight": 100,
            "details": {
                "product_name": "product3",
                "proteins_100g": 20,
                "fats_100g": 15,
            },
        }
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client_no_user.put(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/{ingredient.id}",
            json=payload,
        )
        assert response.status_code == 401

    async def test_update_meal_ingredient_wrong_meal_id(
        self, client, sample_meal_with_ingredient
    ):
        payload = {
            "weight": 100,
            "details": {
                "product_name": "product3",
                "proteins_100g": 20,
                "fats_100g": 15,
            },
        }
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client.put(
            f"/meals/99999/ingredients/{ingredient.id}", json=payload
        )
        assert response.status_code == 404

    async def test_update_meal_ingredient_wrong_ingredient_id(
        self, client, sample_meal_with_ingredient
    ):
        payload = {
            "weight": 100,
            "details": {
                "product_name": "product3",
                "proteins_100g": 20,
                "fats_100g": 15,
            },
        }
        response = await client.put(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/99999", json=payload
        )
        assert response.status_code == 404

    async def test_update_meal_ingredient_wrong_data(
        self, client, sample_meal_with_ingredient
    ):
        payload = {
            "weight": 100,
            "details": {
                "product_name": "product3",
                "proteins_100g": 20,
                "fats_100g": -4,
            },
        }
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client.put(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/{ingredient.id}",
            json=payload,
        )
        assert response.status_code == 422

    # --- DELETE /meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_delete_meal_ingredient_success(
        self, client, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client.delete(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingredient.id

    async def test_delete_meal_ingredient_no_auth(
        self, client_no_user, sample_meal_with_ingredient
    ):
        ingredient = sample_meal_with_ingredient.ingredients[0]
        response = await client_no_user.delete(
            f"/meals/{sample_meal_with_ingredient.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 401

    async def test_delete_meal_ingredient_wrong_ids(self, client):
        response = await client.delete("/meals/9999/ingredients/9999")
        assert response.status_code == 404
