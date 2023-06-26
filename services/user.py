from http.client import HTTPException

from asyncpg import UniqueViolationError
from passlib.context import CryptContext

from db import database
from services.auth import AuthService
from models import user, RoleType
from services.helpers import HelperService

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
    async def make_admin(user_id):
        user_data = await HelperService.get_user_by_id(user_id)
        if user_data["role"] is RoleType.approver:
            await UserService.remove_approver(user_id, RoleType.admin)
        else:
            await database.execute(
                user.update().where(user.c.id == user_id).values(role=RoleType.admin)
            )

    @staticmethod
    async def make_approver_with_company(user_id, company_id):
        # Check that the user exists in the DB.
        user_data = await HelperService.get_user_by_id(user_id)
        if user_data["role"] is RoleType.approver:
            raise HTTPException(400, f"The user {user_data['id']} role is already an approver for company {user_data['company_id']}.")

        # Update user role and company ID in the DB.
        await database.execute(
            user.update().where(user.c.id == user_id).values(role=RoleType.approver, company_id=company_id)
        )

    @staticmethod
    async def remove_approver(user_id, role: RoleType):
        user_data = await HelperService.get_user_by_id(user_id)
        if user_data["role"] is not RoleType.approver:
            raise HTTPException(400, f"The user {user_id} role isn't an approver.")

        # Update user role and company ID in the DB.
        await database.execute(
            user.update().where(user.c.id == user_id).values(role=role, company_id=None)
        )

    @staticmethod
    async def remove_admin(user_id):
        user_data = await HelperService.get_user_by_id(user_id)
        if user_data["role"] is not RoleType.admin:
            raise HTTPException(400, f"The user {user_id} role isn't an admin.")

        # Update user role and company ID in the DB.
        await database.execute(
            user.update().where(user.c.id == user_id).values(role=RoleType.candidate)
        )

