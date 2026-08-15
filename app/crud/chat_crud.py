from sqlalchemy.orm import Session

from app import models, schemas

# Create conversation
def create_conversation(
        db: Session,
        conversation: schemas.ConversationCreate,
        user_id:int
):
    new_conversation=models.Conversation(
        title=conversation.title,
        user_id=user_id
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation

# Get all conversations of a user

def get_user_conversations(
        db:Session,
        user_id:int
):
    return(
        db.query(models.Conversation).filter(models.Conversation.user_id==user_id).all()
    )

# Get one conversation
def get_conversation(
    db: Session,
    conversation_id: int,
    user_id: int
):
    return(
        db.query(models.Conversation).filter(models.Conversation.id== conversation_id,
                 models.Conversation.user_id==user_id).first()
    )


# Update conversation
def update_conversation(
    db: Session,
    conversation_id: int,
    user_id: int,
    conversation: schemas.ConversationCreate
):
    existing_conversation=(
        db.query(models.Conversation).filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        ).first()
    )

    if existing_conversation is None:
        return None

    existing_conversation.title= conversation.title

    db.commit()
    db.refresh(existing_conversation)

    return existing_conversation


# Delete conversation
def delete_conversation(
    db: Session,
    conversation_id: int,
    user_id: int
):
    existing_conversation = (
        db.query(models.Conversation)
        .filter(
            models.Conversation.id == conversation_id,
            models.Conversation.user_id == user_id
        )
        .first()
    )

    if existing_conversation is None:
        return None

    db.delete(existing_conversation)
    db.commit()

    return existing_conversation