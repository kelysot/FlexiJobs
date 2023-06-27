from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from schemas.request.job import JobIn
from schemas.response.job import JobOut
from services.auth import oauth2_scheme, is_approver
from services.job import JobService

router = APIRouter(tags=["Jobs"])


@router.get(
    "/jobs/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[JobOut],
)
async def get_all_jobs(request: Request):
    user = request.state.user
    return await JobService.get_all_jobs(user)


@router.post(
    "/jobs/",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    response_model=JobOut,
    status_code=201,
)
async def create_job(request: Request, job: JobIn):
    user = request.state.user
    return await JobService.create_job(job.dict(), user)
