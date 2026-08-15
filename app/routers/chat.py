from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, crud, models
from app.auth import get_current_user

router=APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# Create conversation
@router.post("/conversations",response_model=schemas.ConversationResponse)
def create_conversation(
    conversation: schemas.ConversationCreate,
    db: Session =Depends(get_db),
    current_user:models.User = Depends(get_current_user)
):
    return crud.create_conversation(
        db,
        conversation,
        current_user.id
    )

# Get all my conversations
@router.get(
    "/conversations",
    response_model=list[schemas.ConversationResponse]
)
def get_my_conversations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return crud.get_user_conversations(
        db,
        current_user.id
    )

# Get one conversation
@router.get(
    "/conversations/{conversation_id}",
    response_model=schemas.ConversationResponse
)
def get_my_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    conversation = crud.get_conversation(
        db,
        conversation_id,
        current_user.id
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    return conversation


# Update conversation
@router.put(
    "/conversations/{conversation_id}",
    response_model=schemas.ConversationResponse
)
def update_my_conversation(
    conversation_id: int,
    conversation: schemas.ConversationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_conversation = crud.update_conversation(
        db,
        conversation_id,
        current_user.id,
        conversation
    )

    if updated_conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )
    return updated_conversation


# Delete conversation
@router.delete("/conversations/{conversation_id}")
def delete_my_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_conversation = crud.delete_conversation(
        db,
        conversation_id,
        current_user.id
    )

    if deleted_conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return {
        "message": "Conversation deleted successfully"
    }