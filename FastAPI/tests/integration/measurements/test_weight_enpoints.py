import pytest


@pytest.mark.integration
class TestWeightEndpoints:
    async def test_add_user_success(self, client):
        response = await client.post("/weights", json={"weight": 80})

        assert response.status_code == 200

    async def test_add_user_wrong_data(self, client):
        response = await client.post("/weights", json={"weight": -5})

        assert response.status_code == 422

    async def test_add_user_no_auth(self, client_no_user):
        response = await client_no_user.post("/weights", json={"weight": 80})

        assert response.status_code == 401

    async def test_read_current_weight_success(self, client, sample_weights):
        response = await client.get("/weights/current")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_weights[-1].id
        assert data["weight"] == sample_weights[-1].weight
        assert data["date"] == str(sample_weights[-1].date)

    async def test_read_current_weight_no_auth(self, client_no_user, sample_weight):
        response = await client_no_user.get("/weights/current")

        assert response.status_code == 401

    async def test_read_current_weight_no_weights(self, client):
        response = await client.get("/weights/current")

        assert response.status_code == 200
        assert response.json() is None

    async def test_read_previous_weight_success(self, client, sample_weights):
        response = await client.get("/weights/previous")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_weights[-2].id
        assert data["weight"] == sample_weights[-2].weight
        assert data["date"] == str(sample_weights[-2].date)

    async def test_read_previous_weight_no_auth(self, client_no_user, sample_weights):
        response = await client_no_user.get("/weights/previous")

        assert response.status_code == 401

    async def test_read_previous_weight_no_weights(self, client):
        response = await client.get("/weights/previous")

        assert response.status_code == 200
        assert response.json() is None

    async def test_read_user_weight_success(self, client, sample_weight):
        response = await client.get(f"/weights/{sample_weight.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_weight.id
        assert data["weight"] == sample_weight.weight
        assert data["date"] == str(sample_weight.date)

    async def test_read_user_weight_not_existent_id(self, client, sample_weight):
        response = await client.get("/weights/99")

        assert response.status_code == 404

    async def test_read_user_weight_other_users_weight(
        self, client, sample_weight_other_user
    ):
        response = await client.get(f"/weights/{sample_weight_other_user.id}")

        assert response.status_code == 404

    async def test_read_user_weight_wrong_id(self, client, sample_weight):
        response = await client.get("/weights/abc")

        assert response.status_code == 422

    async def test_read_user_weight_no_auth(self, client_no_user, sample_weight):
        response = await client_no_user.get(f"/weights/{sample_weight.id}")

        assert response.status_code == 401

    async def test_read_user_weights_success(self, client, sample_weights):
        response = await client.get("/weights")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

        first = data[0]
        assert "id" in first
        assert "weight" in first
        assert "date" in first

    async def test_read_user_weights_no_auth(self, client_no_user, sample_weights):
        response = await client_no_user.get("/weights")

        assert response.status_code == 401

    async def test_read_user_weights_no_weights(self, client):
        response = await client.get("/weights")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    async def test_delete_weight_route_success(self, client, sample_weight):
        response = await client.delete(f"/weights/{sample_weight.id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_weight.id
        assert data["weight"] == sample_weight.weight
        assert data["date"] == str(sample_weight.date)

    async def test_delete_weight_route_no_auth(self, client_no_user, sample_weight):
        response = await client_no_user.delete(f"/weights/{sample_weight.id}")

        assert response.status_code == 401

    async def test_delete_weight_route_non_existent_id(self, client, sample_weight):
        response = await client.delete("/weights/999")

        assert response.status_code == 404

    async def test_delete_weight_route_other_users_weight(
        self, client, sample_weight_other_user
    ):
        response = await client.delete(f"/weights/{sample_weight_other_user.id}")

        assert response.status_code == 404

    async def test_delete_weight_route_wrong_data(self, client, sample_weight):
        response = await client.delete("/weights/asd")

        assert response.status_code == 422
