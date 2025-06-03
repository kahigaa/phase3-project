import pytest
from db.database import SessionLocal, Base, engine
from controllers import user_controller

@pytest.fixture
def session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(session):
    user = user_controller.create_user(session, name="Alice")
    assert user.name == "Alice"
    assert isinstance(user.id, int)

def test_list_users(session):
    user_controller.create_user(session, name="Bob")
    users = user_controller.list_users(session)
    assert any(u.name == "Bob" for u in users)
