from sqlalchemy.orm import Session
from myapp.models.goal import Goal

def set_goal(session: Session, user_id: int, daily: int, weekly: int) -> Goal:
    goal = session.query(Goal).filter(Goal.user_id == user_id).first()
    if goal:
        goal.daily = daily
        goal.weekly = weekly
    else:
        goal = Goal(user_id=user_id, daily=daily, weekly=weekly)
        session.add(goal)
    session.commit()
    return goal

def list_goals(session: Session, user_id: int):
    """List goals for a specific user."""
    return session.query(Goal).filter(Goal.user_id == user_id).all()