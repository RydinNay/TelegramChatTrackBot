from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

from config import DB_URL

engine = create_async_engine(DB_URL, echo=False)
async_session = sessionmaker(bind = engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
