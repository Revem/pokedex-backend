from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_pokemons():
    response = client.get("/pokemons/")
    assert response.status_code == 200
    assert response.json()["count"] > 0

def test_get_pokemon_details():
    response = client.get("/pokemons/1")
    assert response.status_code == 200
    assert "name" in response.json()
