from pydantic import BaseModel
import uuid
from fastapi_users import schemas

class PostCreate(BaseModel):
	"""docstring for PostCreate"""
	title: str
	content: str

class PostResponse(BaseModel):
	"""docstring for PostResponse"""
	title: str
	content: str

class UserRead(schemas.BaseUser[uuid.UUID]):
	pass

class UserCreate(schemas.BaseUserCreate):
	pass

class UserUpdate(schemas.BaseUserUpdate):
	pass
