from fastapi import APIRouter
from routes import auth

api_router = APIRouter()
api_router.include_router(auth.router)
