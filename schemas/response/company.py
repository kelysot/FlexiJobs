from schemas.base import BaseCompany


class CompanyOut(BaseCompany):
    id: int
    logo_url: str
