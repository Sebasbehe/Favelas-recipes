from pydantic import BaseModel


class RecipeCreate(BaseModel):
    """
    Schema used to create a recipe.
    """

    title: str
    ingredients: str
    steps: str
    difficulty: str
    estimated_time: str
    user_id: int


class RecipeResponse(BaseModel):
    """
    Schema returned when a recipe is retrieved.
    """

    id: int
    title: str
    ingredients: str
    steps: str
    difficulty: str
    estimated_time: str
    user_id: int

    class Config:
        from_attributes = True
