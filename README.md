# Generador de Recetas con IA

Aplicación web desarrollada con FastAPI que permite gestionar ingredientes, generar recetas utilizando inteligencia artificial y almacenar calificaciones de los usuarios.

## Tecnologías

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker
- OpenRouter

## Requisitos previos

Antes de ejecutar el proyecto, asegúrese de tener instalado:

Python 3.10 o superior
PostgreSQL
Docker Desktop
Git

## Instalación
1. Clonar el repositorio
        git clone https://github.com/Sebasbehe/Favelas-recipes.git

2. Crear y activar un entorno virtual:
python -m venv venv        

3. Instalar dependencias:
pip install -r requirements.txt

```bash
docker-compose up --build
```

## Variables de entorno

Revisar `.env.example`

## Endpoints

- /auth
- /ingredients
- /recipes
- /ratings

## Swagger

/docs