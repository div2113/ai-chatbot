from pydantic import BaseModel ,EmailStr
from typing import Optional

class UserBase(BaseModel):
    username:str
    email:EmailStr

class UserCreate(UserBase):
    password: str
    

class UserUpdate(UserBase):
    username: str | None = None
    email: EmailStr | None = None

    model_config = {
        "from_attributes": True
    }

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    is_admin: bool

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token:str
    refresh_token: str
    token_type: str

class RefreshtokenRequest(BaseModel):
    refresh_token: str

class ChangePassword(BaseModel):
    old_password: str
    new_password:str

