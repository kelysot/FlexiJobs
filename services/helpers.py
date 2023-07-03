from http.client import HTTPException

from db import database
from models import user, company, job, job_user


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

    # -------------------------------- Job Helper --------------------------------
    @staticmethod
    async def get_job_by_id(job_id):
        query = job.select().where(job.c.id == job_id)
        result = await database.fetch_one(query)

        # Check if the user id that the method got exist in the DB.
        if result is None:
            raise HTTPException(404, f"The job with ID {job_id} doesn't exist in the DB.")

        return dict(result)

    # -------------------------------- Job User Helper --------------------------------

    @staticmethod
    async def get_job_user_by_id(job_id, candidate_id):
        # Check if the candidate_id and job_id that the method got exist in the DB.
        await HelperService.get_user_by_id(candidate_id)
        await HelperService.get_job_by_id(job_id)

        query = job_user.select().where(job_user.c.job_id == job_id).where(job_user.c.candidate_id == candidate_id)
        result = await database.fetch_one(query)

        # Check if the candidate applied to the job.
        if result is None:
            raise HTTPException(404, f"The candidate {candidate_id} didn't apply for the job with the ID {job_id}.")

        return dict(result)

    @staticmethod
    async def get_job_candidate_company_data(job_user_data):
        # Check if the candidate_id and job_id that the method got exist in the DB.
        await HelperService.get_job_user_by_id(job_user_data['job_id'], job_user_data['candidate_id'])

        # Find the all data about the job, the candidate, and the company.
        job_data = await HelperService.get_job_by_id(job_user_data["job_id"])
        candidate_data = await HelperService.get_user_by_id(job_user_data["candidate_id"])
        company_data = await HelperService.get_company_by_id(job_data['company_id'])

        return job_data, candidate_data, company_data
