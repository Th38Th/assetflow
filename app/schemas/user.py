from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class TokenWithRefresh(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str

class UserInDB(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True