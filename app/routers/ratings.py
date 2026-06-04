from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.database import get_db
from app.auth import get_current_user
from app.models import User, Recipe, Rating

router = APIRouter(prefix="/api/ratings", tags=["ratings"])

class RatingCreate(BaseModel):
    score: float = Field(ge=1, le=5, description="Calificación de 1 a 5 estrellas")
    comment: Optional[str] = ""


@router.post("/{recipe_id}")
async def rate_recipe(
    recipe_id: int,
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calificar una receta (1-5 estrellas)"""
    
    # Verificar que la receta existe y pertenece al usuario
    recipe = db.query(Recipe).filter(
        Recipe.id == recipe_id,
        Recipe.user_id == current_user.id
    ).first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    # Buscar si ya existe una calificación
    existing_rating = db.query(Rating).filter(
        Rating.recipe_id == recipe_id,
        Rating.user_id == current_user.id
    ).first()
    
    if existing_rating:
        # Actualizar calificación existente
        existing_rating.score = rating_data.score
        existing_rating.comment = rating_data.comment
        db.commit()
        return {"message": "Calificación actualizada", "rating": existing_rating}
    else:
        # Crear nueva calificación
        new_rating = Rating(
            score=rating_data.score,
            comment=rating_data.comment,
            user_id=current_user.id,
            recipe_id=recipe_id
        )
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        return {"message": "Calificación agregada", "rating": new_rating}


@router.get("/{recipe_id}")
async def get_rating(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener la calificación del usuario para una receta"""
    
    rating = db.query(Rating).filter(
        Rating.recipe_id == recipe_id,
        Rating.user_id == current_user.id
    ).first()
    
    if not rating:
        return {"has_rating": False, "rating": None}
    
    return {"has_rating": True, "rating": rating}


@router.delete("/{recipe_id}")
async def delete_rating(
    recipe_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Eliminar calificación de una receta"""
    
    rating = db.query(Rating).filter(
        Rating.recipe_id == recipe_id,
        Rating.user_id == current_user.id
    ).first()
    
    if not rating:
        raise HTTPException(status_code=404, detail="Calificación no encontrada")
    
    db.delete(rating)
    db.commit()
    
    return {"message": "Calificación eliminada"}
