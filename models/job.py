import sqlalchemy

from db import metadata
from models.enums import Category

job = sqlalchemy.Table(
    "jobs",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(120), nullable=False),
    sqlalchemy.Column("description", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("location", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("hourly_rate", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("skills", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("working_hours", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column(
        "company_id", sqlalchemy.ForeignKey("companies.id"), nullable=False
    ),
    sqlalchemy.Column(
        "category",
        sqlalchemy.Enum(Category),
        nullable=False,
        server_default=Category.other.name,
    ),
    sqlalchemy.Column(
        "posted_date", sqlalchemy.DateTime, server_default=sqlalchemy.func.now()
    ),
)
