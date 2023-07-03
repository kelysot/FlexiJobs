from sqlalchemy import Table, Column, ForeignKey, DateTime, Enum, Date

from db import metadata
from models.enums import Status

job_user = Table(
    "jobs_users",
    metadata,
    Column("job_id", ForeignKey("jobs.id"), primary_key=True),
    Column("candidate_id", ForeignKey("users.id"), primary_key=True),
    Column(
        "status",
        Enum(Status),
        nullable=False,
        server_default=Status.pending.name,
    ),
    Column("start_day", Date, nullable=True),
    Column("salary_day", Date, nullable=True),

)
