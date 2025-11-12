from sqlalchemy import Table, Column, Integer, String, Float, Text
from .db import metadata

skills = Table(
    "skills",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("skill_name", String, nullable=False),
    Column("resource_type", String),
    Column("platform", String),
    Column("progress", String, default="started"),
    Column("hours_spent", Float, default=0.0),
    Column("notes", Text),
    Column("difficulty_rating", Integer, default=3),
)
