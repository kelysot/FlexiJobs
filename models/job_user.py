from sqlalchemy import Table, Column, ForeignKey

from db import metadata

job_user = Table(
    "jobs_users",
    metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("candidate_id", ForeignKey("users.id"), primary_key=True),
)
