from pydantic import BaseModel

class PostCreate(BaseModel):
	"""docstring for PostCreate"""
	title: str
	content: str

class PostResponse(BaseModel):
	"""docstring for PostResponse"""
	title: str
	content: str