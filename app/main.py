
from fastapi import FastAPI
from fastapi import Request

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import Base
from app.database import engine

from app.routers.auth import router as auth_router
from app.routers.ingredients import router as ingredients_router
from app.routers.recipes import router as recipes_router
from app.routers.ratings import router as ratings_router

import app.models
import time

time.sleep(10)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Generador de Recetas"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)

app.include_router(auth_router)
app.include_router(ingredients_router)
app.include_router(recipes_router)
app.include_router(ratings_router)

@app.get("/")
def root():
    return {
        "message": "API funcionando"
    }

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )
