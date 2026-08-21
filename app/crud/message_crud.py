from sqlalchemy.orm import Session
from app.services.llm_service import generate_response
from app import models, schemas
from requests.exceptions import RequestException



# Create message
def create_message(
    db: Session,
    message: schemas.MessageCreate,
    conversation_id: int,
    user_id: int
):
    # Check that the conversation belongs to the current user
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if conversation is None:
        return None

    user_message = models.Message(
        role ="user" ,
        content=message.content,
        conversation_id=conversation_id
    )

    db.add(user_message)
    db.commit()
    db.refresh(user_message)

    try:
        ai_response = generate_response(message.content)
    except Exception:
        raise
    
    assistant_message = models.Message(
        role="assistant",
        content=ai_response,
        conversation_id=conversation_id
    )

    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)


    return {
        "user_message": user_message,
        "assistant_message": assistant_message
    }


# Get all messages in a conversation
def get_messages(
    db: Session,
    conversation_id: int,
    user_id: int,
    skip: int =0,
    limit: int =20
):
    # Verify conversation ownership first
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if conversation is None:
        return None

    return (
        db.query(models.Message)
        .filter(
            models.Message.conversation_id == conversation_id
        )
        .order_by(models.Message.created_at.asc())
        .offset(skip)
        .limit(limit)
        .all()
    )


# Get one message
def get_message(
    db: Session,
    message_id: int,
    conversation_id: int,
    user_id: int
):
    # Verify conversation ownership
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if conversation is None:
        return None

    return (
        db.query(models.Message)
        .filter(
            models.Message.id == message_id,
            models.Message.conversation_id == conversation_id
        )
        .first()
    )


# Update message
def update_message(
    db: Session,
    message_id: int,
    conversation_id: int,
    user_id: int,
    message: schemas.MessageCreate
):
    # Verify conversation ownership
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if conversation is None:
        return None

    existing_message = (
        db.query(models.Message)
        .filter(
            models.Message.id == message_id,
            models.Message.conversation_id == conversation_id
        )
        .first()
    )

    if existing_message is None:
        return None

    existing_message.content = message.content

    db.commit()
    db.refresh(existing_message)

    return existing_message


# Delete message
def delete_message(
    db: Session,
    message_id: int,
    conversation_id: int,
    user_id: int
):
    # Verify conversation ownership
    conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if conversation is None:
        return None

    existing_message = (
        db.query(models.Message)
        .filter(
            models.Message.id == message_id,
            models.Message.conversation_id == conversation_id
        )
        .first()
    )

    if existing_message is None:
        return None

    db.delete(existing_message)
    db.commit()

    return existing_message