from .database import engine, Base
from myapp.models.user import User
from myapp.models.food_entry import FoodEntry
from myapp.models.goal import Goal
from myapp.models.meal_plan import MealPlan  

def init_db():
    """Drop and recreate all tables."""
    Base.metadata.drop_all(bind=engine)  
    Base.metadata.create_all(bind=engine)  
    print("✅ Database tables dropped and recreated.")

if __name__ == "__main__":
    init_db()