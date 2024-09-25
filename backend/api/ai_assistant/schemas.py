from datetime import datetime
from pydantic import BaseModel


class ChatRecord(BaseModel):
    id: int
    role_type: str
    content: str
    created: datetime


class CompletionRequest(BaseModel):
    """Schems for AI completion request body"""

    question: str
