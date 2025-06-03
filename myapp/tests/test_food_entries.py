import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from myapp.models.food_entry import Base, FoodEntry
from myapp.controllers.foodentry_controller import (
    add_food_entry, list_food_entries, update_food_entry, delete_food_entry
)

@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_add_food_entry(session):
    entry = add_food_entry(session, user_id=1, food="Apple", calories=95, entry_date=date.today())
    assert entry.id is not None
    assert entry.food == "Apple"
    assert entry.calories == 95

def test_list_food_entries(session):
    add_food_entry(session, user_id=2, food="Banana", calories=105, entry_date=date.today())
    add_food_entry(session, user_id=2, food="Orange", calories=62, entry_date=date.today())
    entries = list_food_entries(session, user_id=2)
    assert len(entries) == 2
    foods = [e.food for e in entries]
    assert "Banana" in foods and "Orange" in foods

def test_update_food_entry(session):
    entry = add_food_entry(session, user_id=3, food="Bread", calories=80, entry_date=date.today())
    updated = update_food_entry(session, entry.id, food="Whole Wheat Bread", calories=90, entry_date=None)
    assert updated is True
    updated_entry = session.query(FoodEntry).get(entry.id)
    assert updated_entry.food == "Whole Wheat Bread"
    assert updated_entry.calories == 90

    # Update non-existent id returns False
    assert update_food_entry(session, 9999, food="Nope", calories=0, entry_date=None) is False

def test_delete_food_entry(session):
    entry = add_food_entry(session, user_id=4, food="Milk", calories=150, entry_date=date.today())
    deleted = delete_food_entry(session, entry.id)
    assert deleted is True
    # Confirm deletion
    assert session.query(FoodEntry).get(entry.id) is None

    # Deleting non-existent entry returns False
    assert delete_food_entry(session, 9999) is False

