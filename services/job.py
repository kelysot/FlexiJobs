from http.client import HTTPException

from db import database
from models import RoleType, job, company_job
from services.company import CompanyService


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
        if user["company_id"] is None:
            raise HTTPException(400, f"The approver {user['id']} doesn't have a company that he belongs to.")

        job_data["company_id"] = user['company_id']

        # Will create the job, company_job and update company data only if everything is successful.
        async with database.transaction() as conn:
            # Insert job data to job DB.
            id_ = await conn._connection.execute(job.insert().values(job_data))

            # Update company data in the DB.
            company_data = await CompanyService.get_company_by_id(job_data["company_id"])
            company_jobs = company_data.get("jobs", [])
            company_jobs.append(id_)
            company_data["jobs"] = company_jobs
            await CompanyService.update_company_data(company_data["id"], company_data)

            # Insert data to company_job DB.
            company_job_data = {'company_id': job_data["company_id"], 'job_id': id_}
            await conn._connection.execute(company_job.insert().values(company_job_data))

            query = job.select().where(job.c.id == id_)
            result = await conn._connection.fetch_one(query)

            return dict(result)
