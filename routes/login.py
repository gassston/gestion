from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.base import get_db
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import LoginRequest, TokenResponse
from utils.auth import verify_password, create_access_token
from cruds import user
from utils.logger import get_logger


logger = get_logger(__name__)

router = APIRouter(prefix="/login", tags=["Login"])

@router.post("", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.debug(f"Login attempt: username={form_data.username}")

    login_user = user.get_user_by_username(db, form_data.username)
    if not login_user:
        logger.warning(f"Login failed: user '{form_data.username}' not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(form_data.password, login_user.hashed_password):
        logger.warning(f"Login failed: wrong password for user '{form_data.username}'")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    logger.info(f"Login success: user_id={login_user.id}, role={login_user.role}")
    token = create_access_token({"sub": str(login_user.id), "role": login_user.role})
    return {"access_token": token}
