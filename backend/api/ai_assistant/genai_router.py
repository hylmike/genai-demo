from fastapi import APIRouter, Depends

from api.dependencies.auth import valid_is_authenticated
from .schemas import CompletionRequest
from .services import gen_ai_completion

router = APIRouter()


@router.post("/completion", dependencies=[Depends(valid_is_authenticated)])
async def ai_completion(completion_input: CompletionRequest):
    """Generate AI completion for user question, combine info from chat history"""
    completion = await gen_ai_completion(
        completion_input.question, completion_input.chat_history
    )
    return {"completion": completion}
