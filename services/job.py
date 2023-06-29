from http.client import HTTPException

from db import database
from models import RoleType, job


class JobService:

    @staticmethod
    async def get_all_jobs(user):
        q = job.select()

        # Approver will only see the jobs that belong to his company.
        if user["role"] == RoleType.approver:
            q = q.where(job.c.company_id == user["company_id"])

        query_result = database.fetch_all(q)
        return await query_result

    @staticmethod
    async def create_job(job_data, user):
        # Check if the approver that created the new job is allowed to do it.
        if user["role"] != RoleType.approver:
            raise HTTPException(400, f"The user {user['id']} role isn't an approver.")

        job_data["company_id"] = user['company_id']

        # Insert job data to job DB.
        id_ = await database.execute(job.insert().values(job_data))

        query = job.select().where(job.c.id == id_)
        result = await database.fetch_one(query)

        return dict(result)

    @staticmethod
    async def get_jobs_by_company_id(company_id):
        query = job.select().where(job.c.company_id == company_id)
        jobs_data = await database.fetch_all(query)

        return [dict(job_data) for job_data in jobs_data]


