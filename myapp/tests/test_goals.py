import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models.goal import Base, Goal
from myapp.controllers.goal_controller import set_goal, list_goals

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_set_and_update_goal(session):
    # Initially set a goal for user 1
    goal = set_goal(session, user_id=1, daily=2000, weekly=14000)
    assert goal.user_id == 1
    assert goal.daily == 2000
    assert goal.weekly == 14000

    # Update the existing goal for user 1
    updated_goal = set_goal(session, user_id=1, daily=2500, weekly=17500)
    assert updated_goal.id == goal.id  
    assert updated_goal.daily == 2500
    assert updated_goal.weekly == 17500



