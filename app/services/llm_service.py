import httpx
import json
import os
from typing import List, Dict, Any

# Configuración desde variables de entorno
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

async def generate_recipe_from_ingredients(ingredients: List[str]) -> Dict[str, Any]:
    """
    Genera una receta usando OpenRouter basada en la lista de ingredientes
    """
    
    if not OPENROUTER_API_KEY:
        return get_demo_recipe(ingredients)
    
    prompt = f"""
    Eres un chef experto. Tengo los siguientes ingredientes en casa:
    {', '.join(ingredients)}
    
    Por favor, genera una receta que pueda preparar usando estos ingredientes.
    La receta debe estar en formato JSON con la siguiente estructura:
    
    {{
        "nombre": "Nombre del plato",
        "descripcion": "Breve descripción del plato",
        "ingredientes": "Lista de ingredientes con cantidades en formato texto",
        "pasos": "Pasos de preparación enumerados",
        "tiempo": "Tiempo estimado en minutos (solo número)",
        "dificultad": "Fácil, Media o Difícil"
    }}
    
    Responde ÚNICAMENTE con el JSON, sin texto adicional.
    """
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{OPENROUTER_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": "Eres un chef experto que genera recetas en formato JSON."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )
        
        if response.status_code != 200:
            print(f"⚠️ OpenRouter error {response.status_code}: {response.text}")
            return get_demo_recipe(ingredients)
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        
        try:
            recipe = json.loads(content)
            return recipe
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"⚠️ Error parseando respuesta LLM: {e}")
            return get_demo_recipe(ingredients)


def get_demo_recipe(ingredients: List[str]) -> Dict[str, Any]:
    """Devuelve una receta de ejemplo cuando no hay API key disponible"""
    
    ingredients_text = ", ".join(ingredients[:5]) if ingredients else "ingredientes disponibles"
    
    return {
        "nombre": "Salteado Rápido con tus Ingredientes",
        "descripcion": f"Una deliciosa preparación usando {ingredients_text}",
        "ingredientes": "\n".join([f"- {ing}" for ing in ingredients[:5]]),
        "pasos": "1. Preparar todos los ingredientes\n2. Calentar una sartén\n3. Saltear los ingredientes por 5-7 minutos\n4. Servir caliente",
        "tiempo": 20,
        "dificultad": "Fácil"
    }


async def validate_ingredients(ingredients: List[str]) -> Dict[str, Any]:
    """Valida si los ingredientes son suficientes para hacer una receta"""
    
    if not ingredients or len(ingredients) == 0:
        return {"valid": False, "message": "No hay ingredientes registrados"}
    
    if len(ingredients) < 2:
        return {"valid": False, "message": "Necesitas al menos 2 ingredientes para generar una receta"}
    
    return {"valid": True, "message": f"{len(ingredients)} ingredientes disponibles"}
