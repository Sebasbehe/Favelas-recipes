from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.rating import Rating
from app.schemas.rating import RatingCreate

router = APIRouter(
    prefix="/ratings",
    tags=["Ratings"]
)

@router.get("/")
def get_ratings(
    db: Session = Depends(get_db)
):
    return db.query(Rating).all()

@router.post("/")
def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db)
):

    if rating.stars < 1 or rating.stars > 5:
        raise HTTPException(
            status_code=400,
            detail="Las estrellas deben estar entre 1 y 5"
        )

    new_rating = Rating(
        stars=rating.stars,
        recipe_id=rating.recipe_id,
        user_id=rating.user_id
    )

    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)

    return new_rating