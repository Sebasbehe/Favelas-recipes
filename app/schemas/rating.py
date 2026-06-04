from pydantic import BaseModel
from pydantic import Field


class RatingCreate(BaseModel):
    """
    Schema used to create a recipe rating.
    """

    stars: int = Field(
        ge=1,
        le=5
    )

    recipe_id: int
    user_id: int
