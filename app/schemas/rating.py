from pydantic import BaseModel
from pydantic import Field

class RatingCreate(BaseModel):

    stars: int = Field(
        ge=1,
        le=5
    )

    recipe_id: int

    user_id: int