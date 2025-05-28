from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from myapp.base import Base
from sqlalchemy.orm import Session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True , nullable=False)
    name = Column(String, nullable=False, unique=True)

    entries = relationship("FoodEntry", back_populates="user", cascade="all, delete-orphan")
    goal = relationship("Goal", uselist=False, back_populates="user", cascade="all, delete-orphan")
    meal_plans = relationship("MealPlan", back_populates="user", cascade="all, delete-orphan")
@classmethod
def create(cls, db: Session, name: str):
        obj = cls(name=name)
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