from schemas.base import BaseCompany


class CompanyOut(BaseCompany):
    id: int
    photo_url: str
