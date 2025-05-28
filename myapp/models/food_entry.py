from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from myapp.base import Base
from sqlalchemy.orm import Session


class FoodEntry(Base):
    __tablename__ = 'food_entries'

    id = Column(Integer, primary_key=True, nullable=False)  
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False, default=date.today) 

    user = relationship("User", back_populates="entries")

@classmethod
def create(cls, db: Session, user_id: int, food: str, calories: int, date):
        obj = cls(user_id=user_id, food=food, calories=calories, date=date)
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

      