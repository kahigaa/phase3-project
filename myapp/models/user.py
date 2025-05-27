from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")
    goal = relationship("Goal", uselist=False, back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
