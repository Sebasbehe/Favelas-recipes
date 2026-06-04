from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.database import Base, engine
from app.routers import auth, ingredients, recipes, ratings
from app.auth import get_current_user

import app.models
import time
import os
from dotenv import load_dotenv


load_dotenv()


time.sleep(5)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Favelas Recipes - Generador de Recetas con IA",
    description="""
    ## Aplicación web que genera recetas usando inteligencia artificial
    
    ### Funcionalidades:
    * 🔐 Autenticación JWT (registro e inicio de sesión)
    * 📝 CRUD completo de ingredientes
    * 🤖 Generación de recetas con LLM (OpenRouter)
    * ⭐ Sistema de calificaciones (1-5 estrellas)
    * 📜 Historial de recetas generadas
    * 🗑️ Eliminación de recetas
    
    ### Tecnologías:
    * FastAPI (backend)
    * MySQL/PostgreSQL (base de datos)
    * OpenRouter/Groq (LLM)
    * Docker (contenedorización)
    * JWT (autenticación)
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


templates = Jinja2Templates(directory="app/templates")


app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(ingredients.router, prefix="/api/ingredients", tags=["Ingredientes"])
app.include_router(recipes.router, prefix="/api/recipes", tags=["Recetas"])
app.include_router(ratings.router, prefix="/api/ratings", tags=["Calificaciones"])



@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    """Página de inicio con favicon y presentación"""
  
    token = request.cookies.get("access_token")
    user = None
    if token:
        try:
            user = get_current_user(token)
        except:
            pass
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": user,
            "title": "Favelas Recipes"
        }
    )

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Página de inicio de sesión"""
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Iniciar Sesión"
        }
    )

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Página de registro de usuarios"""
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Registro de Usuario"
        }
    )

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """Panel principal del usuario (requiere autenticación)"""
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Mi Dashboard"
        }
    )

@app.get("/ingredients", response_class=HTMLResponse)
async def ingredients_page(request: Request):
    """Página para gestionar el inventario de ingredientes"""
    return templates.TemplateResponse(
        "ingredients.html",
        {
            "request": request,
            "title": "Mis Ingredientes"
        }
    )

@app.get("/generate-recipe", response_class=HTMLResponse)
async def generate_recipe_page(request: Request):
    """Página para generar recetas con IA"""
    return templates.TemplateResponse(
        "generate_recipe.html",
        {
            "request": request,
            "title": "Generar Receta con IA"
        }
    )

@app.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    """Página de historial de recetas generadas"""
    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "title": "Historial de Recetas"
        }
    )

@app.get("/recipe/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail_page(request: Request, recipe_id: int):
    """Página de detalle de una receta específica"""
    return templates.TemplateResponse(
        "recipe_detail.html",
        {
            "request": request,
            "request": request,
            "recipe_id": recipe_id,
            "title": "Detalle de Receta"
        }
    )



@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Manejo personalizado de errores HTTP"""
    if exc.status_code == 404:
        return templates.TemplateResponse(
            "404.html",
            {"request": request},
            status_code=404
        )
    elif exc.status_code == 403:
        return templates.TemplateResponse(
            "403.html",
            {"request": request},
            status_code=403
        )
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": exc.detail},
        status_code=exc.status_code
    )



@app.get("/health", tags=["Sistema"])
async def health_check():
    """Endpoint para verificar que el servicio está funcionando"""
    return {
        "status": "healthy",
        "service": "Favelas Recipes",
        "version": "1.0.0"
    }

@app.get("/api", tags=["Sistema"])
async def api_info():
    """Información general de la API"""
    return {
        "name": "Favelas Recipes API",
        "version": "1.0.0",
        "documentation": "/docs",
        "endpoints": {
            "auth": "/api/auth",
            "ingredients": "/api/ingredients",
            "recipes": "/api/recipes",
            "ratings": "/api/ratings"
        }
    }



if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
