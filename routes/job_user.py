from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from schemas.request.job_user import JobUserApprove
from schemas.response.user import UserOut
from services.auth import oauth2_scheme, is_candidate, is_approver
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


@router.get(
    "/jobs_users/{job_id}/get-candidates-by-job-id/",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    response_model=List[UserOut],
)
async def get_candidates_by_job_id(request: Request, job_id: int):
    user = request.state.user
    return await JobUserService.get_candidates_by_job_id(user, job_id)


@router.put(
    "/jobs_users/{candidate_id}/approve",
    dependencies=[Depends(oauth2_scheme), Depends(is_approver)],
    status_code=204,
)
async def approve_candidate(request: Request, job_user: JobUserApprove):
    approver = request.state.user
    await JobUserService.approve(approver, job_user.dict())
