from sqlalchemy.orm import Session
from myapp.models.meal_plan import MealPlan
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_meal_plan(session: Session, user_id: int, week: int) -> MealPlan:
    """Create a new meal plan."""
    try:
        plan = MealPlan.create(session, user_id=user_id, week=week)
        logger.info(f"Meal plan created for user_id={user_id}, week={week}")
        return plan
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to create meal plan: {e}")
        raise

def update_meal_plan(session: Session, id: int, week: Optional[int]) -> bool:
    """Update an existing meal plan."""
    try:
        plan = session.query(MealPlan).filter(MealPlan.id == id).first()
        if not plan:
            logger.warning(f"Meal plan with ID {id} not found.")
            return False
        if week:
            plan.week = week
        session.commit()
        logger.info(f"Meal plan with ID {id} updated.")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to update meal plan with ID {id}: {e}")
        raise

def delete_meal_plan(session: Session, id: int) -> bool:
    """Delete a meal plan."""
    try:
        plan = session.query(MealPlan).filter(MealPlan.id == id).first()
        if not plan:
            logger.warning(f"Meal plan with ID {id} not found.")
            return False
        plan.delete(session)
        logger.info(f"Meal plan with ID {id} deleted.")
        return True
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to delete meal plan with ID {id}: {e}")
        raise