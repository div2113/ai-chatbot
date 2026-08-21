from pydantic import BaseModel ,EmailStr, Field
from typing import Optional
from datetime import datetime

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

class ConversationCreate(BaseModel):
    title: str | None = Field(
    default=None,
    min_length=1,
    max_length=100
    )

class ConversationResponse(BaseModel):
    id:int
    title:str |None =None
    summary: str | None = None
    user_id:int

    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=5000
    )


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    conversation_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatResponse(BaseModel):
    user_message : MessageResponse
    assistant_message: MessageResponse