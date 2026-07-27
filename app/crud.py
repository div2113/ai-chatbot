from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import models, schemas
from app.auth import hash_password , verify_password , create_access_token


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user :
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        password = hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db:Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session , user_id:int , user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return None

    if user.email and user.email != db_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user.email).first()

        if existing_user:
            raise HTTPException(
                status_code= status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

    update_data = user.model_dump(exclude_unset=True)

    for key ,value in update_data.items():
        setattr(db_user, key , value)


    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session , user_id:int):
    db_user =db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return None

    db.delete(db_user)
    db.commit()

    return db_user

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
