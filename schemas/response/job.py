from datetime import datetime

from models import Category
from schemas.base import JobBase


class JobOut(JobBase):
    id: int
    posted_date: datetime
