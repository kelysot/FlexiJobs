import sqlalchemy

from db import metadata
from models.enums import Category
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, DateTime, func


job = sqlalchemy.Table(
    "jobs",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(120), nullable=False),
    Column("description", String(255), nullable=False),
    Column("location", String(200), nullable=False),
    Column("hourly_rate", String(200), nullable=False),
    Column("skills", String(200), nullable=False),
    Column("working_hours", String(200), nullable=False),
    Column("company_id", ForeignKey("companies.id"), nullable=False),
    Column(
        "category",
        Enum(Category),
        nullable=False,
        server_default=Category.other.name,
    ),
    Column("posted_date", DateTime, server_default=func.now()),
)
