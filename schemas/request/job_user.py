from datetime import date

from schemas.base import JobUserBase


class JobUserIn(JobUserBase):
    pass


class JobUserApprove(JobUserBase):
    start_day: date
    salary_day: date
