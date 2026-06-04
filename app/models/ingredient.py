from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class Ingredient(Base):

    __tablename__ = "ingredients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        String,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    owner = relationship(
        "User",
        back_populates="ingredients"
    )