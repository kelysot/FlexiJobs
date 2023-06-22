import sqlalchemy
from db import metadata


company_approver = sqlalchemy.Table(
    "company_approvers",
    metadata,
    sqlalchemy.Column("company_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("companies.id")),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)
