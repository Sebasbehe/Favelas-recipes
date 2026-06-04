from fastapi import HTTPException
import json

from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.recipe import Recipe

from app.schemas.recipe import RecipeCreate

from app.models.ingredient import Ingredient

from app.services.llm_service import generate_recipe

router = APIRouter(
    prefix="/recipes",
    tags=["Recipes"]
)

@router.post("/")
def create_recipe(
    recipe: RecipeCreate,
    db: Session = Depends(get_db)
):

    new_recipe = Recipe(
        title=recipe.title,
    ingredients=recipe.ingredients,
    steps=recipe.steps,
    difficulty=recipe.difficulty,
    estimated_time=recipe.estimated_time,
    user_id=recipe.user_id
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return new_recipe


@router.get("/")
def get_recipes(
    db: Session = Depends(get_db)
):

    return db.query(
        Recipe
    ).all()


@router.get("/{recipe_id}")
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):

    recipe = (
        db.query(Recipe)
        .filter(
            Recipe.id == recipe_id
        )
        .first()
    )

    if not recipe:
        return {
            "message": "Receta no encontrada"
        }

    return recipe

@router.post("/generate")
def generate_recipe_endpoint(
    user_id: int,
    db: Session = Depends(get_db)
):

    inventory = (
        db.query(Ingredient)
        .filter(
            Ingredient.user_id == user_id
        )
        .all()
    )

    if not inventory:
        raise HTTPException(
            status_code=404,
            detail="No hay ingredientes registrados"
        )

    recipe_data = generate_recipe(inventory)

    recipe = Recipe(
        title=recipe_data["title"],
        ingredients=json.dumps(
            recipe_data["ingredients"]
        ),
        steps=json.dumps(
            recipe_data["steps"]
        ),
        difficulty=recipe_data["difficulty"],
        estimated_time=recipe_data["estimated_time"],
        user_id=user_id
    )

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe

@router.delete("/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db)
):

    recipe = (
        db.query(Recipe)
        .filter(
            Recipe.id == recipe_id
        )
        .first()
    )

    if not recipe:
        raise HTTPException(
            status_code=404,
            detail="Receta no encontrada"
        )

    db.delete(recipe)
    db.commit()

    return {
        "message": "Receta eliminada"
    }