import pytest
from db.database import SessionLocal, Base, engine
from controllers import meal_plan_controller, user_controller

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_meal_plan(session):
    user = user_controller.create_user(session, name="Eve")
    plan = meal_plan_controller.create_meal_plan(session, user.id, week=22, meals="Pasta, Chicken, Salad")
    assert plan.week == 22
    assert "Pasta" in plan.meals

def test_update_meal_plan(session):
    user = user_controller.create_user(session, name="Frank")
    plan = meal_plan_controller.create_meal_plan(session, user.id, week=23, meals="Old Meals")
    updated = meal_plan_controller.update_meal_plan(session, plan.id, meals="New Meals")
    assert updated.meals == "New Meals"
