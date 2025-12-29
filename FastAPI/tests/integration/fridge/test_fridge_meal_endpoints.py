import pytest


@pytest.mark.integration
class TestFridgeMealEndpoints:
    # --- POST /fridge/meals ---

    async def test_add_fridge_meal_success(self, client_with_fridge):
        payload = {"name": "Toast", "is_favourite": True, "ingredients": []}
        response = await client_with_fridge.post("/fridge/meals", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Toast"
        assert data["is_favourite"] is True

    async def test_add_fridge_meal_no_auth(self, client_no_user):
        payload = {"name": "Toast", "is_favourite": True, "ingredients": []}
        response = await client_no_user.post("/fridge/meals", json=payload)
        assert response.status_code == 401

    async def test_add_fridge_meal_wrong_data(self, client_with_fridge):
        payload = {"name": "", "ingredients": []}
        response = await client_with_fridge.post("/fridge/meals", json=payload)
        assert response.status_code == 422

    # --- GET /fridge/meals ---

    async def test_read_fridge_meals_success(
        self, client_with_fridge, sample_fridge_meal
    ):
        response = await client_with_fridge.get("/fridge/meals")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert any(m["id"] == sample_fridge_meal.id for m in data)

    async def test_read_fridge_meals_no_auth(self, client_no_user):
        response = await client_no_user.get("/fridge/meals")
        assert response.status_code == 401

    # --- GET /fridge/meals/{meal_id} ---

    async def test_read_fridge_meal_success(
        self, client_with_fridge, sample_fridge_meal
    ):
        response = await client_with_fridge.get(
            f"/fridge/meals/{sample_fridge_meal.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_fridge_meal.id

    async def test_read_fridge_meal_wrong_id(self, client_with_fridge):
        response = await client_with_fridge.get("/fridge/meals/9999")
        assert response.status_code == 404

    # --- PUT /fridge/meals/{meal_id} ---

    async def test_update_fridge_meal_success(
        self, client_with_fridge, sample_fridge_meal
    ):
        payload = {"name": "Updated Toast", "is_favourite": False}
        response = await client_with_fridge.put(
            f"/fridge/meals/{sample_fridge_meal.id}", json=payload
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Toast"
        assert data["is_favourite"] is False

    async def test_update_fridge_meal_wrong_data(
        self, client_with_fridge, sample_fridge_meal
    ):
        payload = {"name": ""}  # invalid
        response = await client_with_fridge.put(
            f"/fridge/meals/{sample_fridge_meal.id}", json=payload
        )
        assert response.status_code == 422

    async def test_update_fridge_meal_wrong_id(self, client_with_fridge):
        payload = {"name": "X"}
        response = await client_with_fridge.put("/fridge/meals/9999", json=payload)
        assert response.status_code == 404

    # --- DELETE /fridge/meals/{meal_id} ---

    async def test_delete_fridge_meal_success(
        self, client_with_fridge, sample_fridge_meal
    ):
        response = await client_with_fridge.delete(
            f"/fridge/meals/{sample_fridge_meal.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_fridge_meal.id

    async def test_delete_fridge_meal_wrong_id(self, client_with_fridge):
        response = await client_with_fridge.delete("/fridge/meals/9999")
        assert response.status_code == 404

    # --- GET /fridge/meals/{meal_id}/nutrients/{nutrient_type} ---

    async def test_get_fridge_meal_nutrient_sum_success(
        self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal_id = sample_fridge_meal_with_ingredient.id
        response = await client_with_fridge.get(
            f"/fridge/meals/{meal_id}/nutrients/calories"
        )
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == round(44.5, 0)

    async def test_get_fridge_meal_nutrient_sum_no_ingredients(
        self, client_with_fridge, sample_fridge_meal
    ):
        meal_id = sample_fridge_meal.id
        response = await client_with_fridge.get(
            f"/fridge/meals/{meal_id}/nutrients/calories"
        )
        assert response.status_code == 200
        value = response.json()
        assert isinstance(value, float)
        assert value == 0

    async def test_get_fridge_meal_nutrient_sum_no_auth(
        self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal_id = sample_fridge_meal_with_ingredient.id
        response = await client_no_user.get(
            f"/fridge/meals/{meal_id}/nutrients/calories"
        )
        assert response.status_code == 401

    async def test_get_fridge_meal_nutrient_sum_wrong_meal_id(self, client_with_fridge):
        response = await client_with_fridge.get(
            "/fridge/meals/99999/nutrients/calories"
        )
        assert response.status_code == 404

    async def test_get_fridge_meal_nutrient_sum_invalid_param(
        self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal_id = sample_fridge_meal_with_ingredient.id
        response = await client_with_fridge.get(
            f"/fridge/meals/{meal_id}/nutrients/vitaminC"
        )
        assert response.status_code == 422

    # --- GET /fridge/meals/{meal_id}/macros ---

    async def test_get_fridge_meal_macro_success(
        self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal_id = sample_fridge_meal_with_ingredient.id
        response = await client_with_fridge.get(f"/fridge/meals/{meal_id}/macros")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert all(k in data for k in ["calories", "proteins", "fats", "carbs"])
        assert data["calories"] == round(44.5, 0)
        assert data["proteins"] == round(0.55, 1)
        assert data["fats"] == round(0.15, 1)
        assert data["carbs"] == round(11.5, 1)

    async def test_get_fridge_meal_macro_no_ingredients(
        self, client_with_fridge, sample_fridge_meal
    ):
        meal_id = sample_fridge_meal.id
        response = await client_with_fridge.get(f"/fridge/meals/{meal_id}/macros")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert all(data[k] == 0 for k in ["calories", "proteins", "fats", "carbs"])

    async def test_get_fridge_meal_macro_no_auth(
        self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal_id = sample_fridge_meal_with_ingredient.id
        response = await client_no_user.get(f"/fridge/meals/{meal_id}/macros")
        assert response.status_code == 401

    async def test_get_fridge_meal_macro_wrong_meal_id(self, client_with_fridge):
        response = await client_with_fridge.get("/fridge/meals/99999/macros")
        assert response.status_code == 404
