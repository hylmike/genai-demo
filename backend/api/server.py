import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

from api.database.db import session_manager, create_all_tables
from api.auth.auth_router import router as auth_router
from api.user.users_router import router as users_router
from api.ai_assistant.genai_router import router as genai_router
from api.user.services import create_user, get_all_users
from api.user.schemas import UserForm

load_dotenv()

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Function handles app startup and shutdown events"""
    await create_all_tables()
    # Create default admin user for demo purpose
    async with session_manager.session() as session:
        all_users = await get_all_users(session)
        if len(all_users) == 0:
            await create_user(
                session,
                UserForm(username="admin", password="54321", email="admin@test.com"),
            )
    yield
    if session_manager._engin is not None:
        await session_manager.close()


server = FastAPI(lifespan=lifespan, debug=True)

origins = ["http://localhost:4000"]

server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@server.get("/check_api")
async def check_api():
    return {"status": "Connected to API successfully"}


# Routers
server.include_router(
    users_router,
    prefix="/api/users",
    tags=["users"],
    responses={404: {"description": "Not Found"}},
)
server.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["auth"],
    responses={401: {"description": "You are not authorized"}},
)
server.include_router(
    genai_router,
    prefix="/api/genai",
    tags=["genai"],
    responses={404: {"description": "Not Found"}},
)


if __name__ == "__main__":
    try:
        port = os.environ.get("PORT", 3100)
        uvicorn.run("api.server:server", host="0.0.0.0", port=int(port), reload=True)
    except ValueError:
        print("Failed to start server: port number must be valid integer")
