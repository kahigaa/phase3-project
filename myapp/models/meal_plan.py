from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from myapp.base import Base
from sqlalchemy.orm import Session


class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    week = Column(Integer, nullable=False)
     

    user = relationship("User", back_populates="meal_plans")

@classmethod
def create(cls, db: Session, user_id: int, week_number: int, meal_details: str):
        obj = cls(user_id=user_id, week_number=week_number, meal_details=meal_details)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

def update(self, db: Session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self

def delete(self, db: Session):
        db.delete(self)
        db.commit()
