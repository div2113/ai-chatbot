from fastapi import APIRouter, Depends, HTTPException ,Query
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

# Create message
@router.post(
    "/conversations/{conversation_id}/messages",
    response_model=schemas.ChatResponse
)
def create_message(
    conversation_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    try:
        new_message = crud.create_message(
            db,
            message,
            conversation_id,
            current_user.id
        )

    except Exception as e :
        if str(e) == "Could not connect to Ollama":
            raise HTTPException(
                status_code=503,
                detail="LLM service is currently unavailable"
            )

        if str(e) == "LLM request timed out":
            raise HTTPException(
                status_code=504,
                detail="LLM request timed out"
            )

        raise HTTPException(
            status_code=500,
            detail="LLM request failed"
        )



    if new_message is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return new_message


# Get all messages
@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[schemas.MessageResponse]
)
def get_messages(
    conversation_id: int,
    skip:int = Query(0, ge=0),
    limit: int=Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    messages = crud.get_messages(
        db,
        conversation_id,
        current_user.id,
        skip,
        limit
    )

    if messages is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    return messages


# Get one message
@router.get(
    "/conversations/{conversation_id}/messages/{message_id}",
    response_model=schemas.MessageResponse
)
def get_message(
    conversation_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    message = crud.get_message(
        db,
        message_id,
        conversation_id,
        current_user.id,
        skip,
        limit
    )

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return message


# Update message
@router.put(
    "/conversations/{conversation_id}/messages/{message_id}",
    response_model=schemas.MessageResponse
)
def update_message(
    conversation_id: int,
    message_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    updated_message = crud.update_message(
        db,
        message_id,
        conversation_id,
        current_user.id,
        message
    )

    if updated_message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return updated_message


# Delete message
@router.delete(
    "/conversations/{conversation_id}/messages/{message_id}"
)
def delete_message(
    conversation_id: int,
    message_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    deleted_message = crud.delete_message(
        db,
        message_id,
        conversation_id,
        current_user.id
    )

    if deleted_message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found"
        )

    return {
        "message": "Message deleted successfully"
    }