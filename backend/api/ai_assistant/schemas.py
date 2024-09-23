from pydantic import BaseModel


class ChatRecord(BaseModel):
    role: str
    content: str


class CompletionRequest(BaseModel):
    """Schems for AI completion request body"""

    question: str
    chat_history: list[ChatRecord]
