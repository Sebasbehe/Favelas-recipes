from pydantic import BaseModel
from pydantic import Field


class RatingCreate(BaseModel):
    """
    Schema used to create a recipe rating.
    """

    stars: int = Field(
        ge=1,
        le=5,
        description="Recipe rating from 1 to 5 stars"
    )

    recipe_id: int = Field(
        description="ID of the recipe being rated"
    )

    user_id: int = Field(
        description="ID of the user submitting the rating"
    )
