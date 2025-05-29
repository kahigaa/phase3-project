from myapp.models.food_entry import FoodEntry
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

def add_food_entry(session: Session, user_id: int, food: str, calories: int, entry_date: date):
    entry = FoodEntry(user_id=user_id, food=food, calories=calories, date=entry_date)
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

def list_food_entries(session: Session, user_id: int = None, entry_date: date = None):
    query = session.query(FoodEntry)
    if user_id:
        query = query.filter_by(user_id=user_id)
    if entry_date:
        query = query.filter_by(date=entry_date)
    return query.all()

def update_food_entry(session: Session, id: int, food: Optional[str], calories: Optional[int], entry_date: Optional[str]) -> bool:
    """Update a food entry."""
    # Fetch the food entry by ID
    entry = session.query(FoodEntry).filter(FoodEntry.id == id).first()
    if not entry:
        return False

    # Update fields if provided
    if food:
        entry.food = food
    if calories:
        entry.calories = calories
    if entry_date:
        entry.date = date.fromisoformat(entry_date)

    # Commit the changes
    session.commit()
    return True

def delete_food_entry(session: Session, entry_id: int):
    entry = session.query(FoodEntry).get(entry_id)
    if entry:
        session.delete(entry)
        session.commit()
        return True
    return False
