from pydantic import BaseModel

class RecipeCreate(BaseModel):
    title: str
    ingredients: str
    steps: str
    difficulty: str
    estimated_time: str
    user_id: int


class RecipeResponse(BaseModel):
    id: int
    title: str
    ingredients: str
    steps: str
    difficulty: str
    estimated_time: str
    user_id: int

    class Config:
        from_attributes = True