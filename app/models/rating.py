from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Rating(Base):

    __tablename__ = "ratings"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    stars = Column(Integer)

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="ratings"
    )

    recipe = relationship(
        "Recipe",
        back_populates="ratings"
    )