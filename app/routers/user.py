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

# Register user
@router.post("/", response_model=schemas.UserResponse)
def create_user(
    user : schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db=db , user=user)


# My profile
@router.get("/me", response_model=schemas.UserResponse)
def get_me(
    current_user: User= Depends(get_current_user)
):
    return current_user


# Update my profile
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

# Login
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return crud.login_user(db, form_data)

# Refresh token
@router.post("/refresh")
def refresh_token(
    request: schemas.RefreshtokenRequest,
    db: Session = Depends(get_db)
):
    return crud.refresh_access_token(
        db,
        request.refresh_token
    )

# Change password
@router.put("/change-password")
def change_password(
    passwords: schemas.ChangePassword,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.change_password(
        db,
        current_user,
        passwords
    )

# Logout
@router.post("/logout")
def logout(
    current_user: models.User =Depends(get_current_user)
):
    return{
        "message": "Logout successful"
    }
