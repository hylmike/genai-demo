"""All DB models related to AI assistant and chat management"""

import logging

from sqlalchemy import Column, Integer, String, Text, DateTime, select, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.db import Base


class Chat(Base):
    """Chats table"""

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_type = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created = Column(DateTime, server_default=func.now())
    updated = Column(DateTime, server_default=func.now(), onupdate=func.now())

    @classmethod
    async def create(cls, db: AsyncSession, **kwargs):
        new_chat = cls(**kwargs)
        try:
            db.add(new_chat)
            await db.commit()
            await db.refresh(new_chat)
        except Exception as e:
            logging.exception(f"Failed to insert chat: {e}")
        return new_chat

    @classmethod
    async def find_by_user_id(cls, db: AsyncSession, user_id: int):
        query = await db.execute(select(cls).where(cls.user_id == user_id))
        return query.scalars().all()

    @classmethod
    async def find_human_records(cls, db: AsyncSession, user_id: int):
        query = await db.execute(
            select(cls).where(cls.user_id == user_id, cls.role_type == "HUMAN")
        )
        return query.scalars().all()
