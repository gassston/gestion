from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.base import Base
from cruds import user
from utils.auth import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(Base)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        role = payload.get("role")
        get_user = user.get_user(db, user_id)
        if not get_user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Not authorized")
        return user
    return role_checker
