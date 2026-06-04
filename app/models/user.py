from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )

    ingredients = relationship(
        "Ingredient",
        back_populates="owner"
    )

    recipes = relationship(
        "Recipe",
        back_populates="owner"
    )

    ratings = relationship(
        "Rating",
        back_populates="owner"
    )