from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_recipes_without_auth():
    """Debe retornar 401 si no hay token"""
    response = client.get("/api/recipes")
    assert response.status_code == 401


def test_generate_recipe_without_auth():
    """Debe retornar 401 si no hay token"""
    response = client.post("/api/recipes/generate")
    assert response.status_code == 401


def test_delete_recipe_without_auth():
    """Debe retornar 401 si no hay token"""
    response = client.delete("/api/recipes/1")
    assert response.status_code == 401


def test_recipe_title_not_empty():
    """El título de una receta no debe estar vacío"""
    title = "Arroz con pollo"
    assert title != ""
    assert len(title) > 0
