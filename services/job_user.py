from http.client import HTTPException

from asyncpg import UniqueViolationError
from decouple import config

from APIs.ses import SESService
from db import database
from models import RoleType, job_user
from services.helpers import HelperService

ses = SESService()


class JobUserService:
    @staticmethod
    async def create_job_user(user, job_id):
        # Check that the job exist.
        job = await HelperService.get_job_by_id(job_id)
        company = await HelperService.get_company_by_id(job["company_id"])

        job_user_data = {'job_id': job_id, 'candidate_id': user["id"]}

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


