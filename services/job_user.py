from http.client import HTTPException

from asyncpg import UniqueViolationError

from db import database
from models import RoleType, job_user
from services.helpers import HelperService


class JobUserService:
    @staticmethod
    async def create_job_user(user, job_id):
        # Check that the job exist.
        await HelperService.get_job_by_id(job_id)

        job_user_data = {'job_id': job_id, 'candidate_id': user["id"]}

        # Insert job_user data to job DB.
        try:
            await database.execute(job_user.insert().values(job_user_data))
        except UniqueViolationError:
            raise HTTPException(400, f" The user already applied to the job {job_id}.")


