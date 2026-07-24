from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session

from app.database import Base ,engine , get_db
from app import models , schemas , curd

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Chatbot API"
    }

@app.post("/users" , response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return curd.create_user(db=db , user=user)