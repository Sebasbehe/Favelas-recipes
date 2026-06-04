from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingredient import Ingredient
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientResponse
)
router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"]
)

@router.post("/")
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db)
):

    new_ingredient = Ingredient(
    name=ingredient.name,
    quantity=ingredient.quantity,
    user_id=ingredient.user_id
)

    db.add(new_ingredient)
    db.commit()
    db.refresh(new_ingredient)

    return new_ingredient


@router.get("/")
def get_ingredients(
    db: Session = Depends(get_db)
):
    return db.query(
        Ingredient
    ).all()


@router.put(
    "/{ingredient_id}",
    response_model=IngredientResponse
)
def update_ingredient(
    ingredient_id: int,
    ingredient: IngredientCreate,
    db: Session = Depends(get_db)
):
    db_ingredient = (
        db.query(Ingredient)
        .filter(Ingredient.id == ingredient_id)
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
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db)
):
    db_ingredient = (
        db.query(Ingredient)
        .filter(Ingredient.id == ingredient_id)
        .first()
    )

    if not db_ingredient:
        raise HTTPException(
            status_code=404,
            detail="Ingrediente no encontrado"
        )

    db.delete(db_ingredient)
    db.commit()

    return {
        "message": "Ingrediente eliminado correctamente"
    }