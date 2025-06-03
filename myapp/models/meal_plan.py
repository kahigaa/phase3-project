from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.sqlite import JSON
from myapp.db.database import Base

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week = Column(Integer, nullable=False)
    meals = Column(JSON, nullable=True)  

    user = relationship("User", back_populates="meal_plans")

    @classmethod
    def create(cls, db, user_id: int, week: int, meals: dict):
        """Create a new meal plan."""
        obj = cls(user_id=user_id, week=week, meals=meals)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db, **kwargs):
        """Update an existing meal plan."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self