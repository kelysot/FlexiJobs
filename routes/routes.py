from fastapi import APIRouter
from routes import auth, company, job, user

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(company.router)
api_router.include_router(job.router)
api_router.include_router(user.router)

