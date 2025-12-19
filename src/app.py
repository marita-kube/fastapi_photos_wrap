from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from src.schemas import PostCreate, PostResponse
from src.db import Post, create_database_tables, get_async_session
from src.album import imagekit
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
#from imagekitio import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile


@asynccontextmanager
async def lifespan(app:FastAPI):
	await create_database_tables()
	yield

"""Automatically run lifespan function to create the database models"""
app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
		file: UploadFile = File(...),
		caption: str = Form(""),
		session: AsyncSession = Depends(get_async_session)
):
	"""Create a temporary copy of the uploaded file"""
	
	staging_file_path = None

	try: 
		with tempfile.NamedTemporaryFile(delete=False, dir=tempfile.gettempdir(), suffix=os.path.splitext(file.filename)[1]) as temporary_file:
			staging_file_path = temporary_file.name
			shutil.copyfileobj(file.file, temporary_file)
		with open(staging_file_path, "rb") as f:
			upload_output = imagekit.files.upload(
		        file=f,
		        file_name=file.filename,
		        tags=["uploaded_from_api_backend"]
    )



		upload_output = imagekit.files.upload(
			file=open(staging_file_path, "rb"),
			file_name=file.filename,
			#options=use_unique_file_name=True,
				tags=["uploaded_from_api_backend"]
				

		)

		post = Post(
			caption=caption,
			url=upload_output.url,
			file_type="video" if file.content_type.startswith("video/") else "image",
			file_name= upload_output.name

		)
		session.add(post)
		await session.commit()
		await session.refresh(post)
		return post
	
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))
	finally:
		file.file.close()
	

@app.get("/feed")
async def get_feed(
		session: AsyncSession = Depends(get_async_session)
):
	result = await session.execute(select(Post).order_by(Post.created_at.desc()))
	posts = [row[0] for row in result.all()]

	posts_data = []

	for post in posts:
		posts_data.append(
			{
			"id": str(post.id),
			"caption": post.caption,
			"url": post.url,
			"file_type": post.file_type,
			"file_name": post.file_name,
			"created_at": post.created_at.isoformat()
		}
	)

	return {"posts": posts_data}
