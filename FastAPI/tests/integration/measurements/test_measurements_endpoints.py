import pytest
import datetime as dt

@pytest.mark.integration
class TestMeasurementsEndpoints:

    async def test_add_measurements_success(self, client):
        payload = {
            "weight": {"weight": 80},
            "neck": 40.5,
            "biceps": 35,
            "chest": 110.0,
            "thighs": 65
        }
        response = await client.post("/measurements", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["date"] == str(dt.date.today())
        assert data["weight"]["weight"] == 80
        assert data["neck"] == 40.5
        assert data["biceps"] == 35
        assert data["chest"] == 110.0
        assert data["thighs"] == 65
        assert data["calves"] is None
        assert data["hips"] is None

    async def test_add_measurements_no_auth(self, client_no_user):
        payload = {
            "weight": {"weight": 80},
            "neck": 40.5,
            "biceps": 35,
            "chest": 110.0,
            "thighs": 65
        }
        response = await client_no_user.post("/measurements", json=payload)
        assert response.status_code == 401

    async def test_add_measurements_no_weight(self, client):
        payload = {
            "neck": 40.5,
            "biceps": 35,
            "chest": 110.0,
            "thighs": 65,
            "calves": 35
        }
        response = await client.post("/measurements", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data["id"], int)
        assert data["weight"] is None
        assert data["neck"] == 40.5
        assert data["biceps"] == 35
        assert data["chest"] == 110.0
        assert data["thighs"] == 65
        assert data["calves"] == 35
        assert data["hips"] is None

    async def test_add_measurements_wrong_data(self, client):
        payload = {
            "weight": {"weight": 80},
            "neck": 40.5,
            "biceps": 85,
            "chest": 110.0,
            "thighs": 65
        }
        response = await client.post("/measurements", json=payload)
        assert response.status_code == 422

    async def test_add_measurements_no_data(self, client):
        payload = {}
        response = await client.post("/measurements", json=payload)
        assert response.status_code == 422

    async def test_read_measurement_success(self, client, sample_measurement):
        response = await client.get(f"/measurements/{sample_measurement.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_measurement.id
        assert data["neck"] == sample_measurement.neck
        assert data["chest"] == sample_measurement.chest

    async def test_read_measurement_not_existent_id(self, client):
        response = await client.get("/measurements/999")
        assert response.status_code == 404

    async def test_read_measurement_other_users(self, client, sample_measurement_other_user):
        response = await client.get(f"/measurements/{sample_measurement_other_user.id}")
        assert response.status_code == 404

    async def test_read_measurement_wrong_id(self, client):
        response = await client.get("/measurements/abc")
        assert response.status_code == 422

    async def test_read_measurement_no_auth(self, client_no_user, sample_measurement):
        response = await client_no_user.get(f"/measurements/{sample_measurement.id}")
        assert response.status_code == 401

    async def test_read_latest_measurement_success(self, client, sample_measurements):
        response = await client.get("/measurements/latest")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_measurements[-1].id

    async def test_read_latest_measurement_no_auth(self, client_no_user, sample_measurements):
        response = await client_no_user.get("/measurements/latest")
        assert response.status_code == 401

    async def test_read_latest_measurement_no_data(self, client):
        response = await client.get("/measurements/latest")
        assert response.status_code == 200
        assert response.json() is None

    async def test_read_previous_measurement_success(self, client, sample_measurements):
        response = await client.get("/measurements/previous")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_measurements[-2].id

    async def test_read_previous_measurement_no_auth(self, client_no_user, sample_measurements):
        response = await client_no_user.get("/measurements/previous")
        assert response.status_code == 401

    async def test_read_previous_measurement_no_data(self, client):
        response = await client.get("/measurements/previous")
        assert response.status_code == 200
        assert response.json() is None

    async def test_read_measurements_list_success(self, client, sample_measurements):
        response = await client.get("/measurements")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert "id" in data[0]
        assert "neck" in data[0]

    async def test_read_measurements_list_no_auth(self, client_no_user, sample_measurements):
        response = await client_no_user.get("/measurements")
        assert response.status_code == 401

    async def test_read_measurements_list_no_data(self, client):
        response = await client.get("/measurements")
        assert response.status_code == 200
        assert response.json() == []

    async def test_delete_measurement_success(self, client, sample_measurement):
        response = await client.delete(f"/measurements/{sample_measurement.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == sample_measurement.id

    async def test_delete_measurement_no_auth(self, client_no_user, sample_measurement):
        response = await client_no_user.delete(f"/measurements/{sample_measurement.id}")
        assert response.status_code == 401

    async def test_delete_measurement_non_existent_id(self, client):
        response = await client.delete("/measurements/999")
        assert response.status_code == 404

    async def test_delete_measurement_other_users(self, client, sample_measurement_other_user):
        response = await client.delete(f"/measurements/{sample_measurement_other_user.id}")
        assert response.status_code == 404

    async def test_delete_measurement_wrong_id(self, client):
        response = await client.delete("/measurements/asd")
        assert response.status_code == 422

