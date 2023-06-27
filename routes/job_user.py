from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from services.auth import oauth2_scheme, is_candidate
from services.job_user import JobUserService

router = APIRouter(tags=["JobsUsers"])


@router.post(
    "/jobs_users/",
    dependencies=[Depends(oauth2_scheme), Depends(is_candidate)],
    status_code=201,
)
async def create_job_user(request: Request, job_id: int):
    user = request.state.user
    await JobUserService.create_job_user(user, job_id)
