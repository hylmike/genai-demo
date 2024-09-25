from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from langchain_openai import embeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import bs4
import chromadb
from uuid import uuid4

from .schemas import ChatRecord
from .models import Chat as ChatModel
from api.database.db import AsyncSession

VS_COLLECTION_NAME = "syntax_demo_collection"

vector_store_from_client = None


async def find_human_chat_history(db: AsyncSession, user_id: int):
    chat_human_history = await ChatModel.find_human_records(db, user_id)
    old_chats = [record.content for record in chat_human_history]

    return "\n".join(old_chats)


async def gen_ai_completion(db: AsyncSession, user_id: int, question: str) -> str:
    global vector_store_from_client
    # retrieved_results = vector_store_from_client.similarity_search(question, k=3)
    # retrieved_context = [f"{result.page_content}\n" for result in retrieved_results]

    chat_human_history = await find_human_chat_history(db, user_id)

    await ChatModel.create(db, user_id=user_id, role_type="HUMAN", content=question)

    prompt_template = """Answer the question with your knowledge and following context:
{context}

Question: {question}
"""
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0.01)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = (
        {"context": RunnablePassthrough(), "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    completion = await chain.ainvoke(
        {"question": question, "context": f"{chat_human_history}\n"}
    )
    await ChatModel.create(db, user_id=user_id, role_type="AI", content=completion)

    return completion


async def get_chat_history(db: AsyncSession, user_id: int) -> list[ChatRecord]:
    chat_history = await ChatModel.find_by_user_id(db, user_id)
    return chat_history


def gen_knowledgebase() -> None:
    global vector_store_from_client
    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection(VS_COLLECTION_NAME)

    # For this demo, only parse text in gen-ai page
    strainer = bs4.SoupStrainer("p")
    loader = WebBaseLoader(
        web_path="https://www.syntax.com/managed-services/digital-innovation-services/gen-ai/",
        bs_kwargs={"parse_only": strainer},
    )
    raw_doc = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=[".", ".", " "]
    )
    docs = text_splitter.split_documents(raw_doc)

    collection.add(
        documents=[doc.page_content for doc in docs],
        ids=[str(uuid4()) for _ in range(len(docs))],
    )
    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name=VS_COLLECTION_NAME,
        embedding_function=embeddings,
    )
