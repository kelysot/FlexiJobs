import sqlalchemy
from db import metadata


company_job = sqlalchemy.Table(
    "company_jobs",
    metadata,
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id")),
    sqlalchemy.Column("job_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.id")),
)
