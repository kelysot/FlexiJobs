from http.client import HTTPException

from db import database
from models import user, company, company_approver, RoleType


class HelperService:

    # -------------------------------- User Helper --------------------------------
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

    # -------------------------------- Company Helper --------------------------------
    @staticmethod
    async def get_company_by_id(company_id):
        query = company.select().where(company.c.id == company_id)
        result = await database.fetch_one(query)

        # Check if the user id that the method got exist in the DB.
        if result is None:
            raise HTTPException(404, f"The company with ID {company_id} doesn't exist in the DB.")

        return dict(result)

    @staticmethod
    async def update_company_data(company_id, company_data):
        await database.execute(
            company.update().where(company.c.id == company_id).values(**company_data)
        )

    # -------------------------------- Company_approver Helper --------------------------------
    @staticmethod
    async def get_company_approver_by_user_id(user_id):
        query = company_approver.select().where(company_approver.c.user_id == user_id)
        result = await database.fetch_one(query)

        # Check if the user id that the method got exist in the DB.
        if result is None:
            raise HTTPException(404, f"The company_approver with the user ID {user_id} doesn't exist in the DB.")

        return dict(result)

    @staticmethod
    async def delete(user_id):
        await database.execute(company_approver.delete().where(company_approver.c.user_id == user_id))
