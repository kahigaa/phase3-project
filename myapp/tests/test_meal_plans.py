import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models.meal_plan import Base, MealPlan
from myapp.controllers.meal_controller import create_meal_plan, update_meal_plan, delete_meal_plan

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_meal_plan(session):
    plan = create_meal_plan(session, user_id=1, week=10)
    assert plan.user_id == 1
    assert plan.week == 10
    assert plan.id is not None

def test_update_meal_plan(session):
    plan = create_meal_plan(session, user_id=2, week=12)
    success = update_meal_plan(session, plan.id, week=15)
    assert success
    updated_plan = session.query(MealPlan).get(plan.id)
    assert updated_plan.week == 15

    # Try to update non-existent plan
    success = update_meal_plan(session, id=9999, week=20)
    assert not success

def test_delete_meal_plan(session):
    plan = create_meal_plan(session, user_id=3, week=20)
    success = delete_meal_plan(session, plan.id)
    assert success
    deleted_plan = session.query(MealPlan).get(plan.id)
    assert deleted_plan is None

    # Try to delete non-existent plan
    success = delete_meal_plan(session, id=9999)
    assert not success


