import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_pokemons():
    response = client.get("/v1/pokemons")
    assert response.status_code == 200
