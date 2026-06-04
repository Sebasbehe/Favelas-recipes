# Favelas Recipes 🍳

Aplicación web desarrollada con FastAPI que genera recetas usando inteligencia artificial basándose en los ingredientes disponibles del usuario.

## Tecnologías

- **FastAPI** — backend y API REST
- **PostgreSQL** — base de datos
- **SQLAlchemy** — ORM
- **Docker & Docker Compose** — contenedorización
- **OpenRouter** — servicio LLM para generación de recetas
- **JWT** — autenticación

## Requisitos previos

- Python 3.10 o superior
- Docker Desktop
- Git

## Instalación y ejecución

1. Clonar el repositorio:
```bash
git clone https://github.com/Sebasbehe/Favelas-recipes.git
cd Favelas-recipes
```

2. Copiar las variables de entorno:
```bash
cp .env.example .env
```

3. Editar `.env` y completar los valores:
