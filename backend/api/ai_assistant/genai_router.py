from fastapi import APIRouter, Depends

from api.dependencies.auth import valid_is_authenticated, CurrentUserDep
from .schemas import CompletionRequest
from .services import gen_ai_completion, get_chat_history, gen_knowledgebase
from api.dependencies.db import DBSessionDep

router = APIRouter()


@router.post("/completion")
async def ai_completion(
    completion_input: CompletionRequest,
    db: DBSessionDep,
    user: CurrentUserDep,
):
    """Generate AI completion for user question, combine info from chat history"""
    completion = await gen_ai_completion(db, user.id, completion_input.question)
    return {"completion": completion}


@router.get("/chat-history", dependencies=[Depends(valid_is_authenticated)])
async def chat_history(db: DBSessionDep, user: CurrentUserDep):
    """Load chat history belong to current user"""
    chats = await get_chat_history(db, user.id)

    return {"chat_history": chats}


@router.post("/gen-knowledgebase", dependencies=[Depends(valid_is_authenticated)])
def generate_knowledgebase():
    """Generate RAB knowledge base based on some Syntax web info"""
    gen_knowledgebase()
