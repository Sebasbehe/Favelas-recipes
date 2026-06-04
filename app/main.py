from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth, ingredients, recipes, ratings

import app.models
import time
import os
from dotenv import load_dotenv

load_dotenv()


def wait_for_db(retries=10, delay=3):
    import sqlalchemy.exc

    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Base de datos lista")
            return

        except sqlalchemy.exc.OperationalError as e:
            print(f"ERROR DB: {e}")
            print(f"⏳ Esperando DB... intento {i+1}/{retries}")
            time.sleep(delay)

    raise RuntimeError("❌ No se pudo conectar a la base de datos")


wait_for_db()

app = FastAPI(
    title="Favelas Recipes",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Verifica que exista la carpeta app/static
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(directory="app/templates")

# Routers
app.include_router(auth.router)
app.include_router(ingredients.router)
app.include_router(recipes.router)
app.include_router(ratings.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Favelas Recipes"
        }
    )


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Login"
        }
    )


@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Registro"
        }
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Dashboard"
        }
    )


@app.get("/ingredients", response_class=HTMLResponse)
async def ingredients_page(request: Request):
    return templates.TemplateResponse(
        "ingredients.html",
        {
            "request": request,
            "title": "Ingredientes"
        }
    )


@app.get("/generate-recipe", response_class=HTMLResponse)
async def generate_recipe_page(request: Request):
    return templates.TemplateResponse(
        "generate_recipe.html",
        {
            "request": request,
            "title": "Generar Receta"
        }
    )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Favelas Recipes"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )