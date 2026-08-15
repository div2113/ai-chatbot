from sqlalchemy import Column ,Integer ,String ,Boolean ,ForeignKey
from app.database import Base
from sqlalchemy.orm import Session , relationship 

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