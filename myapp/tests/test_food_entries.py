import pytest
from datetime import date
from db.database import SessionLocal, Base, engine
from controllers import food_entry_controller, user_controller

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_add_food_entry(session):
    user = user_controller.create_user(session, name="Alice")
    entry = food_entry_controller.add_food_entry(
        session, user.id, "Apple", 95, date.today()
    )
    assert entry.food == "Apple"
    assert entry.calories == 95

def test_list_food_entries(session):
    user = user_controller.create_user(session, name="Bob")
    food_entry_controller.add_food_entry(session, user.id, "Orange", 80, date.today())
    entries = food_entry_controller.list_food_entries(session, user.id, date.today())
    assert len(entries) >= 1
    assert entries[0].food == "Orange"
