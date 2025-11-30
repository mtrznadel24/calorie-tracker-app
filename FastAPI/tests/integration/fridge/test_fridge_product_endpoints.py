import pytest


@pytest.mark.integration
class TestFridgeProductEndpoints:
    # --- POST /fridges/{fridge_id}/products ---

    async def test_add_fridge_product_success(self, client_with_fridge, fridge):
        payload = {
            "product_name": "Apple",
            "calories_100g": 52,
            "proteins_100g": 0.3,
            "fats_100g": 0.2,
            "carbs_100g": 14,
            "category": "fruits",
            "is_favourite": True,
        }
        response = await client_with_fridge.post("/fridge/products", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Apple"
        assert data["calories_100g"] == 52
        assert data["category"] == "fruits"
        assert data["is_favourite"] is True

    async def test_add_fridge_product_no_auth(self, client_no_user, fridge):
        payload = {
            "product_name": "Apple",
            "calories_100g": 52,
            "proteins_100g": 0.3,
            "fats_100g": 0.2,
            "carbs_100g": 14,
            "category": "fruits",
            "is_favourite": True,
        }
        response = await client_no_user.post("/fridge/products", json=payload)
        assert response.status_code == 401

    async def test_add_fridge_product_wrong_data(self, client_with_fridge, fridge):
        payload = {
            "product_name": "Apple",
            "calories_100g": -10,  # invalid
            "proteins_100g": 0.3,
            "fats_100g": 0.2,
            "carbs_100g": 14,
            "category": "fruits",
            "is_favourite": True,
        }
        response = await client_with_fridge.post("/fridge/products", json=payload)
        assert response.status_code == 422

    # --- GET /fridges/{fridge_id}/products ---

    async def test_read_fridge_products_success(
        self, client_with_fridge, sample_fridge_product
    ):
        response = await client_with_fridge.get("/fridge/products")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0

    # --- GET /fridges/{fridge_id}/products/{product_id} ---

    async def test_read_fridge_product_success(
        self, client_with_fridge, sample_fridge_product
    ):
        response = await client_with_fridge.get(
            f"/fridge/products/{sample_fridge_product.id}"
        )
        print(response.json())
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_fridge_product.id

    async def test_read_fridge_product_wrong_id(self, client_with_fridge):
        response = await client_with_fridge.get("/fridge/products/9999")
        assert response.status_code == 404

    # --- PUT /fridges/{fridge_id}/products/{product_id} ---

    async def test_update_fridge_product_success(
        self, client_with_fridge, sample_fridge_product
    ):
        payload = {"product_name": "Updated Apple", "calories_100g": 60}
        response = await client_with_fridge.put(
            f"/fridge/products/{sample_fridge_product.id}", json=payload
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == "Updated Apple"
        assert data["calories_100g"] == 60

    async def test_update_fridge_product_wrong_data(
        self, client_with_fridge, sample_fridge_product
    ):
        payload = {"calories_100g": -5}
        response = await client_with_fridge.put(
            f"/fridge/products/{sample_fridge_product.id}", json=payload
        )
        assert response.status_code == 422

    async def test_update_fridge_product_wrong_id(self, client_with_fridge):
        payload = {"product_name": "X"}
        response = await client_with_fridge.put("/fridges/products/9999", json=payload)
        assert response.status_code == 404

    # --- DELETE /fridges/{fridge_id}/products/{product_id} ---

    async def test_delete_fridge_product_success(
        self, client_with_fridge, sample_fridge_product
    ):
        response = await client_with_fridge.delete(
            f"/fridge/products/{sample_fridge_product.id}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_fridge_product.id

    async def test_delete_fridge_product_wrong_id(self, client_with_fridge):
        response = await client_with_fridge.delete("/fridge/products/9999")
        assert response.status_code == 404
