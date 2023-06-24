from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class BaseCompany(BaseModel):
    email: str
    name: str
    description: str
    phone: str
    address: str
