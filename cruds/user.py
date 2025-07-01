from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate
from werkzeug.security import generate_password_hash
from fastapi import HTTPException

def create_user(db: Session, user: UserCreate):
    """Create a new user."""
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if user.email and db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    db_user = User(
        username=user.username,
        name=user.name,
        email=user.email,
        hashed_password=generate_password_hash(user.password),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """Get a user by username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def list_users(db: Session):
    """Get all users."""
    return db.query(User).order_by(User.id.asc())

def update_user(db: Session, user_id: int, update: UserUpdate):
    """Update a user."""
    user = get_user(db, user_id)
    if not user:
        return None
    update_data = update.model_dump(exclude_unset=True)
    if "username" in update_data and update_data["username"]:
        existing_user = db.query(User).filter(User.username == update_data["username"], User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
    if "email" in update_data and update_data["email"]:
        existing_user = db.query(User).filter(User.email == update_data["email"], User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
    if "password" in update_data:
        update_data["hashed_password"] = generate_password_hash(update_data["password"])
        del update_data["password"]
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int):
    """Delete a user."""
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True