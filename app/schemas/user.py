from pydantic import BaseModel
from pydantic import EmailStr


class UserRegister(BaseModel):
    """
    Schema used for user registration.
    """

    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema used for user authentication.
    """

    username: str
    password: str
