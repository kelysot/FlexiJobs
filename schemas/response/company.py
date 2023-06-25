from schemas.base import CompanyBase


class CompanyOut(CompanyBase):
    id: int
    logo_url: str
