import sqlalchemy
from sqlalchemy.orm import relationship, backref

from db import metadata
from models.enums import RoleType

company = sqlalchemy.Table(
    "companies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("email", sqlalchemy.String(120), unique=True),
    sqlalchemy.Column("name", sqlalchemy.String(200)),
    sqlalchemy.Column("description", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("logo_url", sqlalchemy.String(200), nullable=False),
    sqlalchemy.Column("phone", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("address", sqlalchemy.String(20), nullable=False),
    sqlalchemy.Column("approvers", sqlalchemy.ARRAY(sqlalchemy.Integer), nullable=False),
    sqlalchemy.Column("jobs", sqlalchemy.ARRAY(sqlalchemy.Integer), nullable=False),

)
