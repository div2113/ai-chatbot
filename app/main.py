from fastapi import FastAPI , Depends , HTTPException
from sqlalchemy.orm import Session

from app.database import Base ,engine , get_db
from app import models , schemas , crud

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "Welcome to AI Chatbot API"
    }

@app.post("/users" , response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db , user=user)


@app.get("/users", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}" , response_model=schemas.UserResponse)
def get_user(user_id:int , db: Session= Depends(get_db)):
    user =  crud.get_user(db , user_id)

    if user is None:
        raise  HTTPException(
            status_code=404,
            detail = "User not found"
        )

    return user


@app.put("/users/{user.id}", response_model=schemas.UserResponse)
def update_user(
    user_id:int ,
    updated_user: schemas.UserUpdate ,
    db: Session = Depends(get_db)
):
    user = crud.update_user(db , user_id , updated_user)

    if user is None:
        raise HTTPException(
            status_code = 404 ,
            detail ="User not found"
        )

    return user

@app.patch("/users/{user_id}" , response_model=schemas.UserResponse)
def patch_user(
    user_id:int,
    updated_user :schemas.UserPatch ,
    db: Session =Depends(get_db)
):
    user = crud.patch_user(db,user_id , updated_user)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail ="User not found"
        )

    return user

@app.delete("/users/{user_id}")
def delete_user(
    user_id:int,
    db:Session = Depends(get_db)
):
    user=crud.delete_user(db,user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleated successfully"
    }