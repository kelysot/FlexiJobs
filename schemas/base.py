from pydantic import BaseModel

from models import Category


class UserBase(BaseModel):
    email: str


class CompanyBase(BaseModel):
    email: str
    name: str
    description: str
    phone: str
    address: str


class JobBase(BaseModel):
    title: str
    description: str
    location: str
    hourly_rate: str
    skills: str
    working_hours: str
    skills: str
    category: Category

