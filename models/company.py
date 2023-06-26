import sqlalchemy

from db import metadata
from sqlalchemy import Column, Integer, String, Text


company = sqlalchemy.Table(
    "companies",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String(120), unique=True),
    Column("name", String(200)),
    Column("description", Text, nullable=False),
    Column("logo_url", String(200), nullable=False),
    Column("phone", String(20), nullable=False),
    Column("address", String(20), nullable=False),
)
