import os
import uuid

from decouple import config

from db import database
from models import RoleType, company


class CompanyService:
    @staticmethod
    async def get_all_companies():
        q = company.select()
        return await database.fetch_all(q)

    @staticmethod
    async def create_company(company_data, user):
        encoded_photo = company_data.pop("encoded_photo")
        extension = company_data.pop("extension")
        company_data["logo_url"] = "temp"
        id_ = await database.execute(company.insert().values(company_data))
        return await database.fetch_one(company.select().where(company.c.id == id_))
