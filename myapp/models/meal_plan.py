from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from myapp.base import Base


class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week = Column(Integer, nullable=False)
    meals = Column(String, nullable=True)  

    user = relationship("User", back_populates="meal_plans")
