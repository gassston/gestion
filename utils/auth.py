import os
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from enum import Enum
from db.base import get_db
from models.user import User
from utils.logger import get_logger

SECRET_KEY = os.getenv("JWT_KEY")  # Replace with a secure key
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
logger = get_logger(__name__)

class Role(str, Enum):
    user = "user"
    admin = "admin"

class Scope(str, Enum):
    read = "read"
    write = "write"
    admin = "admin"

def hash_password(password: str) -> str:
    """Hash a password using Werkzeug."""
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return check_password_hash(pwhash=hashed_password, password=plain_password)

def validate_scopes(requested_scopes: str) -> list[str]:
    """Validate and return a list of requested scopes."""
    valid_scopes = [scope.value for scope in Scope]
    scopes = requested_scopes.split() if requested_scopes else []
    for scope in scopes:
        if scope not in valid_scopes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid scope: {scope}")
    return scopes

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    """Create a JWT access token with user details."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({
        "exp": expire,
        "email": data.get("email", ""),
        "username": data.get("username", ""),
        "name": data.get("name", "")
    })
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> dict:
    """Get the current user and additional details from the JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        username: str = payload.get("username")
        name: str = payload.get("name")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        logger.debug(f"Returning user data: {user.__dict__}, email={email}, username={username}, name={name}")
        return {
            "user": user,
            "email": email,
            "username": username,
            "name": name
        }
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token") from e

async def get_current_admin(user: dict = Depends(get_current_user)) -> User:
    """Ensure the current user is an admin."""
    if user["user"].role.value != Role.admin.value:
        logger.warning(f"Non-admin user attempted admin access: {user['username']}")
        raise HTTPException(status_code=403, detail="Admin access required")
    return user["user"]