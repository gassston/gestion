from fastapi import APIRouter, Depends, HTTPException, Response, status, Query, Request, Cookie
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timezone, timedelta
from db.base import get_db
from cruds import user, oauth_client
from utils.auth import verify_password, create_access_token, SECRET_KEY, ALGORITHM, validate_scopes
from schemas.auth import OAuth2PasswordRequest, TokenResponse
from utils.logger import get_logger
from fastapi import Form
from typing import Optional
import base64

ACCESS_TOKEN_EXPIRE_MINUTES = 60
router = APIRouter(prefix="/auth", tags=["Auth"])
logger = get_logger(__name__)

@router.post("/token", response_model=TokenResponse)
async def token(
    request: Request,
    response: Response,
    form_data: OAuth2PasswordRequest | None = None,
    grant_type: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    scope: str | None = Form(None),
    client_id: str | None = Form(None),
    client_secret: str | None = Form(None),
    query_grant_type: Optional[str] = Query(None),
    query_username: Optional[str] = Query(None),
    query_password: Optional[str] = Query(None),
    query_scope: Optional[str] = Query(None),
    query_client_id: Optional[str] = Query(None),
    query_client_secret: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Authenticate a user and issue an OAuth 2.0 access token."""
    # Log request details for debugging
    logger.debug(f"Request headers: {dict(request.headers)}")
    logger.debug(f"Request query params: {dict(request.query_params)}")
    logger.debug(f"Form data: {form_data.model_dump() if form_data else {'grant_type': grant_type, 'username': username, 'password': password, 'scope': scope, 'client_id': client_id, 'client_secret': client_secret}}")

    # Extract client_id and client_secret from Authorization header if present
    auth_header = request.headers.get("authorization")
    header_client_id = None
    header_client_secret = None
    if auth_header and auth_header.startswith("Basic "):
        try:
            encoded_credentials = auth_header.split(" ")[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
            header_client_id, header_client_secret = decoded_credentials.split(":")
            logger.debug(f"Extracted client_id from Authorization header: {header_client_id}")
        except (base64.binascii.Error, ValueError, UnicodeDecodeError) as e:
            logger.warning(f"Invalid Authorization header: {e}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header")

    # Prioritize form/JSON data, fall back to query params
    if form_data:
        data = form_data
    elif grant_type or username or password or scope or client_id or client_secret:
        data = OAuth2PasswordRequest(
            grant_type=grant_type,
            username=username,
            password=password,
            scope=scope,
            client_id=client_id,
            client_secret=client_secret
        )
    elif query_grant_type or query_username or query_password:
        logger.warning("Using query parameters for token request (non-standard)")
        data = OAuth2PasswordRequest(
            grant_type=query_grant_type or "",
            username=query_username or "",
            password=query_password or "",
            scope=query_scope,
            client_id=query_client_id,
            client_secret=query_client_secret
        )
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No valid input provided")

    # Override client_id and client_secret if provided in Authorization header
    final_client_id = header_client_id if header_client_id else data.client_id
    final_client_secret = header_client_secret if header_client_secret else data.client_secret

    logger.debug(f"Processed request data: {data.dict()}")
    logger.debug(f"Final client credentials: client_id={final_client_id}, client_secret={'[REDACTED]' if final_client_secret else None}")

    # Validate grant_type
    if data.grant_type != "password":
        logger.warning(f"Invalid grant type: {data.grant_type}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid grant type")

    # Validate client credentials
    if not final_client_id or not final_client_secret:
        logger.warning("Missing client_id or client_secret")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Client authentication required")
    oauth_client.validate_oauth_client(db, final_client_id, final_client_secret)

    # Validate user credentials
    login_user = user.get_user_by_username(db, data.username)
    if not login_user or not verify_password(login_user.hashed_password, data.password):
        logger.warning(f"Login failed for {data.username}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user credentials")

    # Validate scopes
    scopes = validate_scopes(data.scope) if data.scope else []

    # Create access token
    token_data = {
        "sub": str(login_user.id),
        "role": login_user.role.value,
        "scope": " ".join(scopes) if scopes else None
    }
    access_token = create_access_token(
        token_data,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    # Set token as cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False,  # Set to True in production
        path="/"
    )

    logger.info(f"Token issued for {data.username}")
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        "scope": data.scope
    }

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
    access_token: str = Cookie(None),
    db: Session = Depends(get_db)
):
    """Refresh the JWT token."""
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        role = payload.get("role")
        scope = payload.get("scope")

        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        exp = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
        now = datetime.now(timezone.utc)

        if exp < now:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

        new_token = create_access_token(
            {"sub": user_id, "role": role, "scope": scope},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        response.set_cookie(
            key="access_token",
            value=new_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax",
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            path="/"
        )

        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            "scope": scope
        }

    except JWTError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e