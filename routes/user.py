from fastapi import APIRouter, Depends

from models import RoleType
from services.auth import oauth2_scheme, is_admin
from services.user import UserService

router = APIRouter(tags=["Users"])


@router.put(
    "/users/{user_id}/make-admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_admin(user_id: int):
    await UserService.make_admin(user_id)


@router.put(
    "/users/{user_id}/make-approver-with-company",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_approver_with_company(user_id: int, company_id: int):
    await UserService.make_approver_with_company(user_id, company_id)


@router.put(
    "/users/{user_id}/make-approver",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def make_approver(user_id: int):
    await UserService.make_approver(user_id)


@router.put(
    "/users/{user_id}/remove-approver",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def remove_approver(user_id: int, role: RoleType):
    await UserService.remove_approver(user_id, role)


@router.put(
    "/users/{user_id}/remove-admin",
    dependencies=[Depends(oauth2_scheme), Depends(is_admin)],
    status_code=204,
)
async def remove_admin(user_id: int):
    await UserService.remove_admin(user_id)
