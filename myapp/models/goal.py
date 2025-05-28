from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from myapp.base import Base
from sqlalchemy.orm import Session


class Goal(Base):
    __tablename__ = 'goals'

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    daily = Column(Integer, nullable=False)
    weekly = Column(Integer, nullable=False)

    user = relationship("User", back_populates="goal")
    
    
@classmethod
def create(cls, db: Session, user_id: int, daily_calories: int, weekly_calories: int):
        obj = cls(user_id=user_id, daily_calories=daily_calories, weekly_calories=weekly_calories)
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