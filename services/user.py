import random
import uuid
from http.client import HTTPException
from typing import Dict

from asyncpg import UniqueViolationError
from decouple import config
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

    @staticmethod
    async def get_users_by_ids(user_ids):
        query = user.select().where(user.c.id.in_(user_ids))
        result = await database.fetch_all(query)
        fetched_ids = [row["id"] for row in result]

        # Check if all user ids that the method got exist in the DB.
        if set(user_ids) != set(fetched_ids):
            non_existing_ids = set(user_ids) - set(fetched_ids)
            raise HTTPException(400, f"The following user IDs don't exist: {non_existing_ids}")

        return [dict(row) for row in result]

    @staticmethod
    async def get_user_by_id(user_id):
        query = user.select().where(user.c.id == user_id)
        result = await database.fetch_one(query)

        # Check if the user id that the method got exist in the DB.
        if result is None:
            raise HTTPException(404, f"The user with ID {user_id} doesn't exist in the DB.")

        return dict(result)

    @staticmethod
    async def update_user_data(user_id, user_data):
        await database.execute(
            user.update().where(user.c.id == user_id).values(**user_data)
        )
