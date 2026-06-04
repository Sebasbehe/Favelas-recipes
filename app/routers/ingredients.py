from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Ingredient

router = APIRouter(
    prefix="/api/ingredients",
    tags=["ingredients"]
)

# Schemas

class IngredientCreate(BaseModel):
    name: str
    quantity: str = ""


class IngredientResponse(BaseModel):
    id: int
    name: str
    quantity: str

    class Config:
        from_attributes = True


@router.get("/", response_model=List[IngredientResponse])
async def get_ingredients(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ingredients = (
        db.query(Ingredient)
        .filter(Ingredient.user_id == current_user.id)
        .all()
    )

    return ingredients


@router.post("/", response_model=IngredientResponse)
async def create_ingredient(
    ingredient: IngredientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_ingredient = Ingredient(
        name=ingredient.name,
        quantity=ingredient.quantity,
        user_id=current_user.id
    )

    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient


@router.put("/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_ingredient = (
        db.query(Ingredient)
        .filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == current_user.id
        )
        .first()
    )

    if not db_ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    db_ingredient.name = ingredient.name
    db_ingredient.quantity = ingredient.quantity

    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


@router.delete("/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    ingredient = (
        db.query(Ingredient)
        .filter(
            Ingredient.id == ingredient_id,
            Ingredient.user_id == current_user.id
        )
        .first()
    )

    if not ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    db.delete(ingredient)
    db.commit()

    return {
        "message": "Ingrediente eliminado correctamente"
    }


@router.get("/stats")
async def get_ingredient_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total = (
        db.query(Ingredient)
        .filter(
            Ingredient.user_id == current_user.id
        )
        .count()
    )

    return {
        "total": total
    }