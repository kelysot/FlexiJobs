from datetime import datetime, timezone
from http.client import HTTPException

import pytz
from asyncpg import UniqueViolationError
from decouple import config
from sqlalchemy import DateTime

from APIs.ses import SESService
from db import database
from models import job_user, Status
from services.helpers import HelperService

ses = SESService()


class JobUserService:
    @staticmethod
    async def create_job_user(user, job_id):
        # Check that the job exist.
        job = await HelperService.get_job_by_id(job_id)
        company = await HelperService.get_company_by_id(job["company_id"])

        job_user_data = {'job_id': job_id, 'candidate_id': user["id"], 'status': Status.pending}

        # Insert job_user data to job DB.
        try:
            await database.execute(job_user.insert().values(job_user_data))
        except UniqueViolationError:
            raise HTTPException(400, f" The user already applied to the job {job_id}.")

        # Send a mail to the user that shows that his submission for the job was successful.
        ses.send_mail(
            f"Thank you for your submission to {company['name']}",
            [config("EMAIL_SENDER")],
            f"Dear {user['first_name']},\n\nThank you for your interest in {job['title']} position.\n"
            f"We're always looking for top talent and we're glad that you're considering us for your next role.\n"
            f"If our team feels your skills and experience are a good fit for this opportunity, we'll reach out.\n"
            f"We appreciate your interest in working with us!\nSincerely,\n{company['name']} \n",
        )

    @staticmethod
    async def get_candidates_by_job_id(user, job_id):
        job = await HelperService.get_job_by_id(job_id)

        # Check if the approver belongs to the company that the job belongs to.
        if job["company_id"] != user["company_id"]:
            raise HTTPException(404, f"The approver doesn't belong to the company {job['company_id']} "
                                     f"that the job {job_id} belongs to.")

        query = job_user.select().where(job_user.c.job_id == job_id)
        jobs_users_data = await database.fetch_all(query)

        # Check if the user id that the method got exist in the DB.
        if jobs_users_data is None:
            raise HTTPException(404, f"The job with ID {job_id} doesn't exist in the DB.")

        # Extract the candidate IDs from the result list.
        candidate_ids = [row['candidate_id'] for row in jobs_users_data]
        result = await HelperService.get_users_by_ids(candidate_ids)

        return result

    @staticmethod
    async def approve(approver, job_user_data):
        # Find the all data about the job, the candidate, and the company.
        job = await HelperService.get_job_by_id(job_user_data["job_id"])
        candidate = await HelperService.get_user_by_id(job_user_data["candidate_id"])
        company = await HelperService.get_company_by_id(job['company_id'])

        # Check if the approver belongs to the company that the job belongs to.
        if job["company_id"] != approver["company_id"]:
            raise HTTPException(404, f"The approver doesn't belong to the company {job['company_id']} "
                                     f"that the job {job_user_data['job_id']} belongs to.")

        # Update the job_user data in the DB.
        await database.execute(
            job_user.update()
            .where(job_user.c.job_id == job_user_data["job_id"])
            .where(job_user.c.candidate_id == job_user_data["candidate_id"])
            .values(status=Status.approved, start_day=job_user_data["start_day"],
                    salary_day=job_user_data["salary_day"],)
        )

        # Email the candidate to tell him that he got the job.
        ses.send_mail(
            f"Welcome to {company['name']} {candidate['first_name']}!",
            [config("EMAIL_SENDER")],
            f"Dear {candidate['first_name']},\n\n"
            f"On behalf of the entire team at {company['name']}, I am thrilled to extend a warm welcome to you!\n "
            f"We are delighted that you have accepted our job offer for the position of {job['title']}.\n\n  "
            f"Warm regards,\n \n "
            f"{approver['first_name']}\n "
            f"{company['name']}",
        )




