from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
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

    generated_by_ai = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="recipes"
    )

    ratings = relationship(
        "Rating",
        back_populates="recipe"
    )
