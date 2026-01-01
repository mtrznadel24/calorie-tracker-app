import pytest


@pytest.mark.integration
class TestMealEndpoints:
    # --- POST /meals ---

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
        assert isinstance(data["id"], int)
        assert data["type"] == "breakfast"
        assert data["weight"] == 50
        assert data["calories"] == 150

    async def test_add_meal_log_no_auth(self, client_no_user):
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
        response = await client_no_user.post("/meals/quick", json=payload)
        assert response.status_code == 401

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

    # --- GET /meals/{meal_id} ---

    async def test_read_meal_by_id_success(self, client, sample_meal_log):
        response = await client.get(f"/meals/{sample_meal_log.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_meal_log.id
        assert data["type"] == "breakfast"

    async def test_read_meal_by_id_no_auth(self, client_no_user, sample_meal_log):
        response = await client_no_user.get(f"/meals/{sample_meal_log.id}")
        assert response.status_code == 401

    async def test_read_meal_by_id_not_found(self, client):
        response = await client.get("/meals/99999")
        assert response.status_code == 404

    # POST /{meal_date}/{meal_type}/ingredients/from-fridge-product/{fridge_product_id}

    # async def test_add_fridge_product_to_meal_success(
    #     self, client_with_fridge, fridge_product_factory
    # ):
    #     product = await fridge_product_factory(
    #         product_name="Product1",
    #         calories_100g=150,
    #         proteins_100g=25,
    #         fats_100g=10,
    #         carbs_100g=40,
    #         category=FoodCategory.FRUIT,
    #         is_favourite=False,
    #     )
    #     payload = {"weight": 50}
    #     response = await client_with_fridge.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-product/{product.id}",
    #         json=payload,
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["weight"] == 50
    #     assert isinstance(data["id"], int)
    #     details = data["details"]
    #     assert details["product_name"] == "Product1"
    #     assert details["calories_100g"] == 150
    #
    # async def test_add_fridge_product_to_meal_success_meal_exits(
    #     self, client_with_fridge, sample_meal, fridge_product_factory
    # ):
    #     product = await fridge_product_factory(
    #         product_name="Product1",
    #         calories_100g=150,
    #         proteins_100g=25,
    #         fats_100g=10,
    #         carbs_100g=40,
    #         category=FoodCategory.FRUIT,
    #         is_favourite=False,
    #     )
    #     payload = {"weight": 50}
    #     response = await client_with_fridge.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-product/{product.id}",
    #         json=payload,
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert data["weight"] == 50
    #     assert isinstance(data["id"], int)
    #     details = data["details"]
    #     assert details["product_name"] == "Product1"
    #     assert details["calories_100g"] == 150
    #
    #     async def test_add_fridge_product_to_meal_success_meal_exits(
    #         self, client_with_fridge, sample_meal, fridge_product_factory
    #     ):
    #         product = await fridge_product_factory(
    #             product_name="Product1",
    #             calories_100g=150,
    #             proteins_100g=25,
    #             fats_100g=10,
    #             carbs_100g=40,
    #             category=FoodCategory.FRUIT,
    #             is_favourite=False,
    #         )
    #         payload = {"weight": 50}
    #         response = await client_with_fridge.post(
    #             f"/meals/{date(2022, 1, 1)}/"
    #             f"{MealType.BREAKFAST.value}/"
    #             f"ingredients/from-fridge-product/{product.id}",
    #             json=payload,
    #         )
    #         assert response.status_code == 200
    #         data = response.json()
    #         assert data["weight"] == 50
    #         assert isinstance(data["id"], int)
    #         details = data["details"]
    #         assert details["product_name"] == "Product1"
    #         assert details["calories_100g"] == 150
    #
    # async def test_add_fridge_product_to_meal_no_auth(
    #     self, client_no_user, sample_meal, fridge_product_factory
    # ):
    #     product = await fridge_product_factory(
    #         product_name="Product1",
    #         calories_100g=150,
    #         proteins_100g=25,
    #         fats_100g=10,
    #         carbs_100g=40,
    #         category=FoodCategory.FRUIT,
    #         is_favourite=False,
    #     )
    #     payload = {"weight": 50}
    #     response = await client_no_user.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-product/{product.id}",
    #         json=payload,
    #     )
    #     assert response.status_code == 401
    #
    # async def test_add_fridge_product_to_meal_wrong_product_id(
    #     self, client_with_fridge, sample_meal, fridge_product_factory
    # ):
    #     payload = {"weight": 50}
    #     response = await client_with_fridge.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-product/99999",
    #         json=payload,
    #     )
    #     assert response.status_code == 404

    # - POST /{meal_date}/{meal_type}/ingredients/from-fridge-meal/{fridge_meal_id} -

    # TODO fix later
    # async def test_add_fridge_meal_to_meal_success(
    #     self,
    #     client_with_fridge,
    #     fridge_product_factory,
    #     fridge_meal_factory,
    #     fridge_meal_ingredient_factory,
    # ):
    #     fridge_meal = await fridge_meal_factory(meal_name="Meal1")
    #     fridge_products = [
    #         await fridge_product_factory(
    #             product_name=name,
    #             calories_100g=150,
    #             proteins_100g=25,
    #             fats_100g=10,
    #             carbs_100g=40,
    #             category=FoodCategory.FRUIT,
    #             is_favourite=False,
    #         )
    #         for name in ["Product1", "Product2", "Product3"]
    #     ]
    #     [
    #         await fridge_meal_ingredient_factory(fridge_meal, 50, prod)
    #         for prod in fridge_products
    #     ]
    #
    #     payload = {"weight": 50}
    #     response = await client_with_fridge.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-meal/{fridge_meal.id}",
    #         json=payload,
    #     )
    #     assert response.status_code == 200
    #     data = response.json()
    #     assert isinstance(data, list)
    #
    #     assert len(data) == 3
    #
    #     for i, ingredient in enumerate(data):
    #         assert isinstance(ingredient["id"], int)
    #         assert ingredient["weight"] == 17.0
    #
    #         details = ingredient["details"]
    #         assert details["product_name"] == f"Product{i + 1}"
    #         assert details["calories_100g"] == 150.0
    #         assert details["proteins_100g"] == 25.0
    #         assert details["fats_100g"] == 10.0
    #         assert details["carbs_100g"] == 40.0

    # async def test_add_fridge_meal_to_meal_no_ingredients(
    #     self,
    #     client_with_fridge,
    #     fridge_product_factory,
    #     fridge_meal_factory,
    #     fridge_meal_ingredient_factory,
    # ):
    #     fridge_meal = await fridge_meal_factory(meal_name="Meal1")
    #
    #     payload = {"weight": 50}
    #     response = await client_with_fridge.post(
    #         f"/meals/{date(2022, 1, 1)}/"
    #         f"{MealType.BREAKFAST.value}/"
    #         f"ingredients/from-fridge-meal/{fridge_meal.id}",
    #         json=payload,
    #     )
    #     assert response.status_code == 404
