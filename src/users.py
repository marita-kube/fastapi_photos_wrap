from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin, models
from fastapi_users.authentication import (AuthenticationBackend, BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase
from src.db import User, get_user_data
import uuid

SECRET = ""

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
	reset_password_token_secret = SECRET
	verification_token_secret = SECRET

	async def on_after_register(self, user:User, request:Optional[Request] = None):
		print(f"{user.id} registered successfully!")

	async def on_after_forgot_password(self, user:User, token:str, request:Optional[Request] = None):
		print(f"{user.id} reset token: {token}")

	async def on_after_request_verify(self, user:User, token: str, request: Optional[Request] = None):
		print(f"{user.id}, verification token: {token}")

async def get_user_manager(user_db: SQLAlchemyUserDatabase=Depends(get_user_data)):
	yield UserManager(user_db)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy():
	return JWTStrategy(secret=SECRET, lifetime_seconds = 3600)

backend_auth = AuthenticationBackend(
	name="jwt",
	transport=bearer_transport,
	get_strategy = get_jwt_strategy)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, auth_backends= [backend_auth])
current_user = fastapi_users.current_user(active=True)