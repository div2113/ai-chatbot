from sqlalchemy.orm import Session
from app import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        email=user.email
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db:Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session , user_id:int , user: schemas.UserUpadte):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return None

    db_user.username = user.username
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user

def patch_user(db: Session , user_id : int , user: schemas.UserPatch):
    db_user= db.query(models.User).filter(models.User.id == user_id).first()

    if db_user is None:
        return None

    if user.username is not None:
        db_user.username = user.username

    if user.email is not None:
        db_user.email = user.email

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