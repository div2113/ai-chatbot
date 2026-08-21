from sqlalchemy import Column ,Integer ,String ,Boolean ,ForeignKey, DateTime
from app.database import Base
from sqlalchemy.orm import Session , relationship 
from datetime import datetime

class User(Base):
    __tablename__ ="users"

    id = Column(Integer, primary_key=True , index=True)
    username = Column(String, nullable=False)
    email = Column(String , unique=True , nullable=False)
    password = Column(String, nullable = False)
    phone_number= Column(String, nullable= True)
    is_admin= Column(Boolean , default=False , nullable=False)
    conversations = relationship("Conversation" , back_populates="user")


class Conversation(Base):
    __tablename__ = "conversations"

    id= Column(Integer , primary_key=True, index=True)
    title= Column(String, nullable=True)
    user_id=Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User" ,back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all , delete-orphan" )

class Message(Base):
    __tablename__ ="messages"

    id = Column(Integer,primary_key=True , index=True)
    role =Column(String , nullable=False)
    content=Column(String , nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    conversation_id= Column(Integer, ForeignKey("conversations.id"), nullable=False)
    conversation = relationship("Conversation" , back_populates="messages")