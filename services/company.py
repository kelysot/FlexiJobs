from http.client import HTTPException

from asyncpg import UniqueViolationError

from db import database
from models import RoleType, company
from services.helpers import HelperService


class CompanyService:
    @staticmethod
    async def get_all_companies():
        q = company.select()
        return await database.fetch_all(q)

    @staticmethod
    async def create_company(company_data):
        encoded_photo = company_data.pop("encoded_photo")
        extension = company_data.pop("extension")
        company_data["logo_url"] = "temp"

        # Try to insert the company data into the DB.
        try:
            id_ = await database.execute(company.insert().values(company_data))
        except UniqueViolationError:
            raise HTTPException(400, f" A company with the email: {company_data['email']} already exists in the DB.")

        return await database.fetch_one(company.select().where(company.c.id == id_))
