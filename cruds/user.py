from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from utils.auth import hash_password


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session):
    return db.query(User).all()

def update_user(db: Session, user_id: int, update: UserUpdate):
    user = get_user(db, user_id)
    if not user:
        return None
    if update.name:
        user.name = update.name
    if update.email:
        user.email = update.email
    if update.password:
        user.hashed_password = hash_password(update.password)
    if update.role:
        user.role = update.role
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
