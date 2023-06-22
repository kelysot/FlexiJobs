import sqlalchemy

from db import metadata
from models.enums import RoleType

user = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column(
        "role",
        sqlalchemy.Enum(RoleType),
        nullable=False,
        server_default=RoleType.candidate.name,
    ),
    sqlalchemy.Column("iban", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column(
        "company_id", sqlalchemy.ForeignKey("companies.id"),
    ),
)
