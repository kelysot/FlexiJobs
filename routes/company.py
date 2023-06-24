from typing import List

from fastapi import APIRouter, Depends
from starlette.requests import Request

from schemas.request.company import CompanyIn
from schemas.response.company import CompanyOut
from services.auth import oauth2_scheme, is_admin
from services.company import CompanyService

router = APIRouter(tags=["Company"])


@router.get(
    "/companies/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[CompanyOut],
)
async def get_all_companies(request: Request):
    # user = request.state.user
    return await CompanyService.get_all_companies()


@router.post(
    "/complaints/",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    response_model=CompanyOut,
)
async def create_company(request: Request, complaint: CompanyIn):
    user = request.state.user
    return await CompanyService.create_company(complaint.dict(), user)
