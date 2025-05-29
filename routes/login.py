from fastapi import APIRouter, Depends, HTTPException, Response, status, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from db.base import get_db
from cruds import user
from utils.auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM
from schemas.auth import TokenResponse
from utils.logger import get_logger

ACCESS_TOKEN_EXPIRE_MINUTES = 60
router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger(__name__)

@router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate a user and set a JWT cookie."""
    logger.debug(f"Login attempt: {form_data.username}")
    login_user = user.get_user_by_username(db, form_data.username)

    if not login_user or not verify_password(hashed_password=login_user.hashed_password, plain_password=form_data.password):
        logger.warning(f"Login failed for {form_data.username}")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": str(login_user.id), "role": login_user.role.value},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,  # Set to True in production
        path="/"
    )

    logger.info(f"Login success for {login_user.username}")
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    """Clear the JWT cookie."""
    response.delete_cookie(
        key="access_token",
        path="/",
        httponly=True,
        samesite="lax",
        secure=False  # Set to True in production
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    response: Response,
    access_token: str = Cookie(None)
):
    """Refresh the JWT token."""
    if not access_token:
        raise HTTPException(status_code=401, detail="No token provided")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)

        if exp < now:
            raise HTTPException(status_code=401, detail="Token expired")

        new_token = create_access_token(
            {"sub": user_id, "role": role},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,
            secure=False,  #TODO: Set to True in production
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )

        return {"access_token": new_token, "token_type": "bearer"}

    except JWTError as e:
        raise HTTPException(status_code=403, detail="Invalid token") from e