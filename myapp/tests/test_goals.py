import pytest
from db.database import SessionLocal, Base, engine
from controllers import goal_controller, user_controller

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_set_goal(session):
    user = user_controller.create_user(session, name="Charlie")
    goal = goal_controller.set_goal(session, user.id, daily=2000, weekly=14000)
    assert goal.daily_calories == 2000
    assert goal.weekly_calories == 14000

def test_list_goals(session):
    user = user_controller.create_user(session, name="Dana")
    goal_controller.set_goal(session, user.id, daily=1800, weekly=12600)
    goals = goal_controller.list_goals(session, user.id)
    assert len(goals) == 1
    assert goals[0].daily_calories == 1800
