from typing import List

from schemas.base import BaseCompany


class CompanyIn(BaseCompany):
    encoded_photo: str
    extension: str
    approvers: List[int]
