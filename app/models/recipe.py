from xmlrpc.client import Boolean

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Recipe(Base):

    __tablename__ = "recipes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(String)

    ingredients = Column(Text)

    steps = Column(Text)

    difficulty = Column(String)

    estimated_time = Column(String)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="recipes"
    )

    ratings = relationship(
        "Rating",
        back_populates="recipe"
    )
    
    generated_by_ai = Column(
    Boolean,
    default=True
)