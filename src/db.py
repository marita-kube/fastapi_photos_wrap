from collections.abc import AsyncGenerator
import uuid
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi import Depends


DATABASE_URL = "sqlite+aiosqlite:///./album_data.db"

"""Handle  DeclarativeBase direct imports in the model"""
class Base(DeclarativeBase):
	"""docstring for Base"""
	pass

"""Define the Users models"""
class User(SQLAlchemyBaseUserTableUUID, Base):
	posts = relationship(argument="Post", back_populates="user")

"""Define the data models"""
class Post(Base):
	__tablename__ = "posts"

	id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
	caption = Column(Text)
	url = Column(String, nullable=False)
	file_type = Column(String, nullable=False)
	file_name = Column(String, nullable=False)
	created_at = Column(DateTime, default=datetime.utcnow)

	user = relationship(argument="User", back_populates="posts")

"""Initialize database engine"""
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit = False)

"""define database and tables creation"""
async def create_database_tables():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session_maker() as session:
		yield session

async def get_user_data(session:AsyncSession = Depends(get_async_session)):
	yield SQLAlchemyUserDatabase(session, User)
