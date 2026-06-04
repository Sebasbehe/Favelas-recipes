import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "deepseek/deepseek-chat-v3-0324:free"
)

def generate_recipe(inventory):

    ingredients_text = "\n".join(
        [
            f"- {item.name}: {item.quantity}"
            for item in inventory
        ]
    )

    prompt = f"""
Genera una receta usando únicamente estos ingredientes:

{ingredients_text}

Responde únicamente en JSON válido.

{{
  "title": "",
  "ingredients": [],
  "steps": [],
  "difficulty": "",
  "estimated_time": ""
}}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    )

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    return json.loads(content)