from fastapi import FastAPI

from app.database import Base
from app.database import engine

from app.routers.auth import router as auth_router
from app.routers.ingredients import router as ingredients_router
from app.routers.recipes import router as recipes_router
from app.routers.ratings import router as ratings_router

import app.models
import time

# Esperar PostgreSQL
time.sleep(10)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI(
    title="Generador de Recetas"
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