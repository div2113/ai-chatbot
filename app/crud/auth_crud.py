from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.auth import hash_password , verify_password , create_access_token


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
        data={"sub":db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type":"bearer"
    }
