from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from .schemas import ChatRecord


async def gen_ai_completion(question: str, chat_history: list[ChatRecord]) -> str:
    prompt_template = """Answer the question with your knowledge and following context:
{context}

Question: {question}
"""
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.01)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    old_chats = [f"{record.role}: {record.content}" for record in chat_history]
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    completion = await chain.ainvoke(
        {"question": question, "context": "\n".join(old_chats)}
    )

    return completion
