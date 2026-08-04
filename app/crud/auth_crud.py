from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.auth import hash_password , verify_password , create_access_token , create_refresh_token , verify_token


def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
    db_user=db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={
            "sub":db_user.email
            }
    )

    refresh_token = create_refresh_token(
        data={
            "sub": db_user.email
        }
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type":"bearer"
    }


def refresh_access_token(
        db: Session,
        refresh_token : str
):
    email = verify_token(refresh_token)

    db_user= db.query(models.User).filter(models.User.email == email).first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = "User not found"
        )

    access_token = create_access_token(
        data={
            "sub": db_user.email
        }
    )
    return {
        "access token": access_token,
        "token_type": "bearer"
    }

def change_password(
        db: Session,
        current_user: models.User,
        passwords: schemas.ChangePassword
):
    if not verify_password(
        passwords.old_password,
        current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )

    current_user.password = hash_password(
        passwords.new_password
    )

    db.commit()
    db.refresh(current_user)

    return {
        "message":"Password changed successfully"
    }