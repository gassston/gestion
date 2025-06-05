from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from utils.auth import SECRET_KEY, ALGORITHM, jwt, get_current_user
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def require_scopes(required_scopes: list[str]):
    """Ensure the user has all required scopes."""
    async def scope_checker(user: User = Depends(get_current_user)):
        try:
            token = await oauth2_scheme(None)
            if not token:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No token provided")
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_scopes = payload.get("scope", "").split()
            for scope in required_scopes:
                if scope not in token_scopes:
                    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Scope {scope} required")
            return user
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from e
    return scope_checker
