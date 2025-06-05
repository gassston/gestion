from pydantic import BaseModel

class OAuth2PasswordRequest(BaseModel):
    grant_type: str
    username: str
    password: str
    scope: str | None = None
    client_id: str | None = None
    client_secret: str | None = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str | None = None