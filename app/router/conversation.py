#Libraries
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List

#Dependencies
import app.authentication.jwt_manager as jwt_manager
from app.database import baseModels
from app.database.database import get_db
from app.database.models import Users, Conversations, Chats, ConversationRole
from app.config.log_config import setup_config
from app.llm.llm import llm_process

#Routing
router = APIRouter(tags=["Conversation"])

#Logging
setup_config()
logger = logging.getLogger(__name__)

@router.post("/conversations", response_model=baseModels.ConversationResponse)
async def create_conversation(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conversation = Conversations(user_id=user.id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation

@router.get("/conversations", response_model=List[baseModels.ConversationResponse])
async def get_conversations(
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conversations = db.query(Conversations).filter_by(user_id=user.id).all()
    return conversations

@router.post("/conversations/{conversation_id}/chats")
async def send_message(
    conversation_id: int,
    chat: baseModels.CreateChat,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify conversation belongs to user
    conversation = db.query(Conversations).filter_by(id=conversation_id, user_id=user.id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message
    user_chat = Chats(
        conversation_id=conversation_id,
        role=ConversationRole.USER,
        content=chat.content
    )
    db.add(user_chat)
    db.commit()
    
    # Process with LLM
    llm_response = await llm_process(chat.content, db)
    
    # Save LLM response
    system_chat = Chats(
        conversation_id=conversation_id,
        role=ConversationRole.SYSTEM,
        content=llm_response
    )
    db.add(system_chat)
    db.commit()
    
    return {"user_message": chat.content, "llm_response": llm_response}

@router.get("/conversations/{conversation_id}/chats", response_model=List[baseModels.ChatResponse])
async def get_conversation_chats(
    conversation_id: int,
    current_user: Annotated[baseModels.Users, Depends(jwt_manager.get_current_user)],
    db: Session = Depends(get_db)
):
    user = db.query(Users).filter_by(username=current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verify conversation belongs to user
    conversation = db.query(Conversations).filter_by(id=conversation_id, user_id=user.id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    chats = db.query(Chats).filter_by(conversation_id=conversation_id).order_by(Chats.create_date).all()
    return chats


