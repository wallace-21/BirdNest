import pytest
from fastapi.testclient import TestClient
from app.core.config import settings


class TestBirdsAPI:

    def test_create_bird(self, client: TestClient, sample_bird_data):
        """
            Test creating a new bird.
        """
        response = client.post(
            f"{settings.API_V1_STR}/birds/",
            json=sample_bird_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["bird_id"] == sample_bird_data["bird_id"]
        assert data["data"]["name"] == sample_bird_data["name"]

    def test_create_duplicate_bird(self, client: TestClient, sample_bird_data):
        """Test creating a bird with duplicate bird_id fails."""
        # Create first bird
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        # Try to create duplicate
        response = client.post(f"{settings.API_V1_STR}/birds/",
                               json=sample_bird_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_read_birds(self, client: TestClient, sample_bird_data):
        """Test reading all birds."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.get(f"{settings.API_V1_STR}/birds/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_bird_by_id(self, client: TestClient, sample_bird_data):
        """Test reading a specific bird by ID."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.get(
            f"{settings.API_V1_STR}/birds/{sample_bird_data['bird_id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["bird_id"] == sample_bird_data["bird_id"]

    def test_read_nonexistent_bird(self, client: TestClient):
        """Test reading a non-existent bird returns 404."""
        response = client.get(f"{settings.API_V1_STR}/birds/nonexistent-bird")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_update_bird(self, client: TestClient, sample_bird_data):
        """Test updating a bird."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        update_data = {"name": "Updated Test Falcon"}
        response = client.put(
            f"{settings.API_V1_STR}/birds/{sample_bird_data['bird_id']}",
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["name"] == "Updated Test Falcon"

    def test_update_nonexistent_bird(self, client: TestClient):
        """Test updating a non-existent bird returns 404."""
        update_data = {"name": "Updated Name"}
        response = client.put(
            f"{settings.API_V1_STR}/birds/nonexistent-bird",
            json=update_data
        )
        assert response.status_code == 404

    def test_delete_bird(self, client: TestClient, sample_bird_data):
        """Test deleting a bird."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.delete(
            f"{settings.API_V1_STR}/birds/{sample_bird_data['bird_id']}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

        # Verify bird is deleted
        response = client.get(
            f"{settings.API_V1_STR}/birds/{sample_bird_data['bird_id']}")
        assert response.status_code == 404

    def test_delete_nonexistent_bird(self, client: TestClient):
        """Test deleting a non-existent bird returns 404."""
        response = client.delete(
            f"{settings.API_V1_STR}/birds/nonexistent-bird")
        assert response.status_code == 404

    def test_search_birds_by_name(self, client: TestClient, sample_bird_data):
        """Test searching birds by name."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.get(
            f"{settings.API_V1_STR}/birds/search/name?name=Test")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "Test" in data[0]["name"]

    def test_search_birds_by_scientific_name(
            self, client: TestClient, sample_bird_data):
        """Test searching birds by scientific name."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.get(
            f"{settings.API_V1_STR}/birds/search/scientific?scientific_name=testicus")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "testicus" in data[0]["scientific_name"]

    def test_filter_birds_by_conservation_status(
            self, client: TestClient, sample_bird_data):
        """Test filtering birds by conservation status."""
        # Create a bird first
        client.post(f"{settings.API_V1_STR}/birds/", json=sample_bird_data)

        response = client.get(
            f"{settings.API_V1_STR}/birds/filter/conservation?status=least-concern")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_search_with_short_query(self, client: TestClient):
        """Test search with too short query returns validation error."""
        response = client.get(
            f"{settings.API_V1_STR}/birds/search/name?name=T")
        assert response.status_code == 422  # Validation error
