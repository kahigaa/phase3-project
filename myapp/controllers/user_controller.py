from myapp.models.user import User
from sqlalchemy.orm import Session

def create_user(session: Session, name: str):
    user = User(name=name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def list_users(session: Session):
    return session.query(User).all()

def get_user_by_name(session: Session, name: str):
    return session.query(User).filter_by(name=name).first()

def delete_user(session: Session, user_id: int):
    user = session.query(User).get(user_id)
    if user:
        session.delete(user)
        session.commit()
        return True
    return False
