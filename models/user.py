import sqlalchemy

from db import metadata
from models.enums import RoleType
from sqlalchemy import Column, ForeignKey, Integer, String, Enum


user = sqlalchemy.Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(120), unique=True),
    Column("password", String(255), nullable=False),
    Column("first_name", String(200), nullable=False),
    Column("last_name", String(200), nullable=False),
    Column("phone", String(20), nullable=False),
    Column(
        "role",
        Enum(RoleType),
        nullable=False,
        server_default=RoleType.candidate.name,
    ),
    Column("iban", String(200), nullable=False),
    Column("company_id", ForeignKey("companies.id")),
)
