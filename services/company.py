import os
import uuid
from http.client import HTTPException

from asyncpg import UniqueViolationError

from APIs.s3 import S3Service
from constants import TEMP_FILE_FOLDER
from db import database
from models import RoleType, company
from services.helpers import HelperService
from utils.helpers import decode_photo

s3 = S3Service()


class CompanyService:
    @staticmethod
    async def get_all_companies():
        q = company.select()
        return await database.fetch_all(q)

    @staticmethod
    async def create_company(company_data):
        # Upload photo to aws S3.
        encoded_photo = company_data.pop("encoded_photo")
        extension = company_data.pop("extension")
        name = f"{uuid.uuid4()}.{extension}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        company_data["logo_url"] = s3.upload(path, name, extension)
        os.remove(path)

        # Try to insert the company data into the DB.
        try:
            id_ = await database.execute(company.insert().values(company_data))
        except UniqueViolationError:
            raise HTTPException(400, f" A company with the email: {company_data['email']} already exists in the DB.")

        return await database.fetch_one(company.select().where(company.c.id == id_))
