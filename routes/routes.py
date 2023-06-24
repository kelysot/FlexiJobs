from fastapi import APIRouter
from routes import auth, company

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(company.router)
