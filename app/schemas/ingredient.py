from pydantic import BaseModel

class IngredientCreate(BaseModel):
    name: str
    quantity: str
    category: str = ""
    user_id: int


class IngredientResponse(BaseModel):
    id: int
    name: str
    quantity: str
    category: str = ""
    user_id: int

    class Config:
        from_attributes = True