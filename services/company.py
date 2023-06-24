import os
import uuid
from http.client import HTTPException

from asyncpg import UniqueViolationError
from decouple import config

from db import database
from models import RoleType, company, company_approver
from services.user import UserService


class CompanyService:
    @staticmethod
    async def get_all_companies():
        q = company.select()
        return await database.fetch_all(q)

    @staticmethod
    async def create_company(company_data):
        # Check that all approvers' data is correct.
        approvers = await UserService.get_users_by_ids(company_data["approvers"])
        for approver in approvers:
            if approver["role"] != RoleType.approver:
                raise HTTPException(400, f"The user {approver['id']} role isn't an approver.")
            if approver["company_id"] is not None:
                raise HTTPException(400, f"The approver {approver['id']} already has a company that he belongs to.")

        encoded_photo = company_data.pop("encoded_photo")
        extension = company_data.pop("extension")
        company_data["logo_url"] = "temp"

        # Try to insert the company data into the DB.
        try:
            id_ = await database.execute(company.insert().values(company_data))
        except UniqueViolationError:
            raise HTTPException(400, f" A company with the email: {company_data['email']} already exists in the DB.")

        # Insert all company and approvers' data to the DB.
        for approver in approvers:
            approver["company_id"] = id_
            await UserService.update_user_data(approver["id"], approver)
            company_approver_data = {'company_id': id_, 'user_id': approver["id"]}
            await database.execute(company_approver.insert().values(company_approver_data))

        return await database.fetch_one(company.select().where(company.c.id == id_))

