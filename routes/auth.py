from fastapi import APIRouter

from schemas.request.user import UserData, UserLoginIn
from services.user import UserService

router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: UserData):
    token = await UserService.register(user_data.dict())
    return {"token": token}


@router.post("/login/")
async def login(user_data: UserLoginIn):
    token, role = await UserService.login(user_data.dict())
    return {"token": token, "role": role}
