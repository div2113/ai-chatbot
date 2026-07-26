from pydantic import BaseModel ,EmailStr
from typing import Optional

class UserBase(BaseModel):
    username:str
    email:EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserPatch(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr

    class Config:
        from_attributes = True

