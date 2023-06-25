from typing import List

from schemas.base import CompanyBase


class CompanyIn(CompanyBase):
    encoded_photo: str
    extension: str
    approvers: List[int]
