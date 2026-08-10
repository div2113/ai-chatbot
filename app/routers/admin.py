from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users" , response_model =list[schemas.UserResponse])
def admin_get_users(
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    return crud.get_users(db)


@router.get("/users/{user_id}", response_model=schemas.UserResponse)
def admin_get_user(
    user_id: int,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.put("/users/{user_id}", response_model=schemas.UserResponse)
def admin_update_user(
    user_id: int,
    updated_user: schemas.UserUpdate,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = crud.update_user(
        db,
        user_id,
        updated_user
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user

@router.delete("/users/{user_id}")
def admin_delete_user(
    user_id : int,
    current_admin: models.User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    if user_id == current_admin.id:
        raise HTTPException(
            status_code=400,
            detail="Admin cannot delete themselves"
        )

    user =crud.delete_user(db,user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
