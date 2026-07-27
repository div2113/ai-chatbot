from fastapi import APIRouter , Depends , HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas , crud , models

from app.auth import get_current_user
from app.models import User

router = APIRouter(
    prefix = "/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user : schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db=db , user=user)


@router.get("/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: User= Depends(get_current_user)
):
    return current_user

@router.get("/{user_id}" , response_model=schemas.UserResponse)
def get_user(user_id:int , db: Session= Depends(get_db)):
    user =  crud.get_user(db , user_id)

    if user is None:
        raise  HTTPException(
            status_code=404,
            detail = "User not found"
        )

    return user

@router.put("/me", response_model = schemas.UserResponse)
def update_current_user(
    updated_user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.update_user(
        db,
        current_user.id,
        updated_user
    )


@router.put("/{user_id}", response_model=schemas.UserResponse)
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

@router.delete("/{user_id}")
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

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return crud.login_user(db, form_data)



