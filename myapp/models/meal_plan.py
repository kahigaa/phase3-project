from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from myapp.db.database import Base
from sqlalchemy.orm import Session


class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    week = Column(Integer, nullable=False)

    user = relationship("User", back_populates="meal_plans")

    @classmethod
    def create(cls, db: Session, user_id: int, week: int):
        """Create a new meal plan."""
        obj = cls(user_id=user_id, week=week)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def update(self, db: Session, **kwargs):
        """Update an existing meal plan."""
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

    def delete(self, db: Session):
        """Delete a meal plan."""
        db.delete(self)
        db.commit()