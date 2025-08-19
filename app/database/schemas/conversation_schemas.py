from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CreateConversation(BaseModel):
    pass

class ConversationResponse(BaseModel):
    id: int
    user_id: int
    create_date: datetime
    model_config = ConfigDict(from_attributes=True)

class CreateChat(BaseModel):
    conversation_id: int
    content: str

class ChatResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    create_date: datetime
    model_config = ConfigDict(from_attributes=True)

class Chat(BaseModel):
    chat: str = ""