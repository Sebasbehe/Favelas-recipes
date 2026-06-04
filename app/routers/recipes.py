from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Recipe, Ingredient, Rating
from app.services.llm_service import generate_recipe_from_ingredients

router = APIRouter(prefix="/api/recipes", tags=["recipes"])

class RecipeCreate(BaseModel):
    name: str
    description: str = ""
    ingredients: str
    steps: str
    prep_time: int = 30
    difficulty: str = "Media"

class RecipeResponse(BaseModel):
    id: int
    name: str
    description: str
    ingredients: str
    steps: str
    prep_time: int
    difficulty: str
    is_favorite: bool
    created_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[RecipeResponse])
async def get_recipes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    favorite_only: bool = False
):
    """Obtener todas las recetas del usuario"""
    query = db.query(Recipe).filter(Recipe.user_id == current_user.id)
    
    if favorite_only:
        query = query.filter(Recipe.is_favorite == True)
    
    recipes = query.order_by(Recipe.created_at.desc()).limit(limit).all()
    return recipes


@router.get("/stats/summary")
async def get_recipe_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas de recetas del usuario"""
    total = db.query(Recipe).filter(Recipe.user_id == current_user.id).count()
    favorites = db.query(Recipe).filter(
        Recipe.user_id == current_user.id,
        Recipe.is_favorite == True
    ).count()
    
    return {
        "total": total,
        "favorites": favorites
    }


@router.post("/generate")
async def generate_recipe(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generar una nueva receta usando IA basada en los ingredientes del usuario"""
    
    ingredients = db.query(Ingredient).filter(
        Ingredient.user_id == current_user.id
    ).all()
    
    if not ingredients:
        raise HTTPException(
            status_code=400, 
            detail="No tienes ingredientes registrados. Agrega ingredientes primero."
        )
    
    ingredient_names = [i.name for i in ingredients]
    
    try:
        recipe_data = await generate_recipe_from_ingredients(ingredient_names)
        
        new_recipe = Recipe(
            name=recipe_data.get("nombre", "Receta Generada"),
            description=recipe_data.get("descripcion", ""),
            ingredients=recipe_data.get("ingredientes", ""),
            steps=recipe_data.get("pasos", ""),
            prep_time=recipe_data.get("tiempo", 30),
            difficulty=recipe_data.get("dificultad", "Media"),
            user_id=current_user.id
        )
        
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        
        return {
            "message": "Receta generada exitosamente",
            "recipe": new_recipe
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generando receta: {str(e)}")


@router.post("/{recipe_id}/favorite")
async def toggle_favorite(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marcar/Desmarcar receta como favorita"""
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    recipe.is_favorite = not recipe.is_favorite
    db.commit()
    
    return {"is_favorite": recipe.is_favorite}


@router.get("/{recipe_id}")
async def get_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener una receta específica"""
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    return recipe


@router.delete("/{recipe_id}")
async def delete_recipe(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar una receta"""
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    db.query(Rating).filter(Rating.recipe_id == recipe_id).delete()
    db.delete(recipe)
    db.commit()
    
    return {"message": "Receta eliminada correctamente"}
