import random
import uuid
from typing import Dict

from asyncpg import UniqueViolationError
from decouple import config
from fastapi import HTTPException
from passlib.context import CryptContext

from db import database
from services.auth import AuthService
from models import user, RoleType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    @staticmethod
    async def register(user_data):
        user_data["password"] = pwd_context.hash(user_data["password"])
        try:
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User with this email already exists")
        new_user = await database.fetch_one(user.select().where(user.c.id == id_))
        return AuthService.encode_token(new_user)

    @staticmethod
    async def login(user_data):
        new_user = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"])
        )
        if not new_user:
            raise HTTPException(400, "Wrong email or password")
        elif not pwd_context.verify(user_data["password"], new_user["password"]):
            raise HTTPException(400, "Wrong email or password")
        return AuthService.encode_token(new_user), new_user["role"]
