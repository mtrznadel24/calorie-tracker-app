import pytest


@pytest.mark.integration
class TestFridgeMealIngredientEndpoints:


    # --- POST fridge/meals/{meal_id}/ingredients ---

    async def test_add_fridge_meal_ingredient_success(self, client_with_fridge, sample_fridge_meal, sample_fridge_product):
        payload = {"weight": 80,
                   "fridge_product_id": sample_fridge_product.id}
        response = await client_with_fridge.post(f"/fridge/meals/{sample_fridge_meal.id}/ingredients", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["weight"] == 80
        assert data["fridge_product_id"] == sample_fridge_product.id

    async def test_add_fridge_meal_ingredient_no_auth(
            self, client_no_user, sample_fridge_meal, sample_fridge_product
    ):
        payload = {
            "weight": 80,
            "fridge_product_id": sample_fridge_product.id,
        }

        response = await client_no_user.post(
            f"/fridge/meals/{sample_fridge_meal.id}/ingredients",
            json=payload,
        )
        assert response.status_code == 401

    async def test_add_fridge_meal_ingredient_wrong_meal(
            self, client_with_fridge, sample_fridge_product
    ):
        payload = {"weight": 50, "fridge_product_id": sample_fridge_product.id}

        response = await client_with_fridge.post(
            "/fridge/meals/99999/ingredients",
            json=payload,
        )
        assert response.status_code == 404

    # --- GET fridge/meals/{meal_id}/ingredients ---

    async def test_read_fridge_meal_ingredients_success(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient

        response = await client_with_fridge.get(
            f"/fridge/meals/{meal.id}/ingredients"
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_read_fridge_meal_ingredients_no_auth(
            self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient

        response = await client_no_user.get(
            f"/fridge/meals/{meal.id}/ingredients"
        )
        assert response.status_code == 401

    async def test_read_fridge_meal_ingredients_wrong_meal(
            self, client_with_fridge
    ):
        response = await client_with_fridge.get(
            "/fridge/meals/99999/ingredients"
        )
        assert response.status_code == 404

    # --- GET fridge/meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_read_fridge_meal_ingredient_success(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        response = await client_with_fridge.get(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingredient.id

    async def test_read_fridge_meal_ingredient_no_auth(
            self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        response = await client_no_user.get(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 401

    async def test_read_fridge_meal_ingredient_wrong_id(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient

        response = await client_with_fridge.get(
            f"/fridge/meals/{meal.id}/ingredients/99999"
        )
        assert response.status_code == 404

    # --- PUT fridge/meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_update_fridge_meal_ingredient_success(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        payload = {"weight": 90}

        response = await client_with_fridge.put(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}",
            json=payload,
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingredient.id
        assert data["weight"] == 90

    async def test_update_fridge_meal_ingredient_no_auth(
            self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        response = await client_no_user.put(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}",
            json={"weight": 123},
        )
        assert response.status_code == 401

    async def test_update_fridge_meal_ingredient_wrong_data(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]
        response = await client_with_fridge.put(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}",
            json={"weight": -2},
        )
        assert response.status_code == 422

    async def test_update_fridge_meal_ingredient_wrong_id(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient

        response = await client_with_fridge.put(
            f"/fridge/meals/{meal.id}/ingredients/99999",
            json={"weight": 100},
        )
        assert response.status_code == 404

    # --- DELETE fridge/meals/{meal_id}/ingredients/{ingredient_id} ---

    async def test_delete_fridge_meal_ingredient_success(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        response = await client_with_fridge.delete(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}"
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == ingredient.id

    async def test_delete_fridge_meal_ingredient_no_auth(
            self, client_no_user, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient
        ingredient = meal.ingredients[0]

        response = await client_no_user.delete(
            f"/fridge/meals/{meal.id}/ingredients/{ingredient.id}"
        )
        assert response.status_code == 401

    async def test_delete_fridge_meal_ingredient_wrong_id(
            self, client_with_fridge, sample_fridge_meal_with_ingredient
    ):
        meal = sample_fridge_meal_with_ingredient

        response = await client_with_fridge.delete(
            f"/fridge/meals/{meal.id}/ingredients/99999"
        )
        assert response.status_code == 404