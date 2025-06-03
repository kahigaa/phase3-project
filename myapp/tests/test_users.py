import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models.user import Base, User
from myapp.controllers.user_controller import create_user, list_users, get_user_by_name, delete_user


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_user(session):
    user = create_user(session, "Alice")
    assert user.id is not None
    assert user.name == "Alice"

def test_list_users(session):
    create_user(session, "Bob")
    create_user(session, "Charlie")
    users = list_users(session)
    assert len(users) == 2
    names = [user.name for user in users]
    assert "Bob" in names and "Charlie" in names

def test_get_user_by_name(session):
    create_user(session, "Diana")
    user = get_user_by_name(session, "Diana")
    assert user is not None
    assert user.name == "Diana"
    missing_user = get_user_by_name(session, "Eve")
    assert missing_user is None

def test_delete_user(session):
    user = create_user(session, "Frank")
    result = delete_user(session, user.id)
    assert result is True
    # Try to get deleted user
    deleted_user = get_user_by_name(session, "Frank")
    assert deleted_user is None

    # Deleting non-existent user returns False
    result = delete_user(session, 9999)
    assert result is False

