from sqlalchemy.orm import Session
from myapp.models.meal_plan import MealPlan

def create_meal_plan(session: Session, user_id: int, week: int, meals: dict) -> MealPlan:
    """Create a new meal plan."""
    plan = MealPlan.create(session, user_id=user_id, week=week, meals=meals)
    return plan

def update_meal_plan(session: Session, id: int, week: int = None, meals: dict = None) -> bool:
    """Update an existing meal plan."""
    plan = session.query(MealPlan).filter(MealPlan.id == id).first()
    if not plan:
        return False
    if week:
        plan.week = week
    if meals:
        plan.meals = meals
    session.commit()
    return True