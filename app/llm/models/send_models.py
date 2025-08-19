from pydantic import BaseModel

class SentChat(BaseModel):
    chat: str = ""