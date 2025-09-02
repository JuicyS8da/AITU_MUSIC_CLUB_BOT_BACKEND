from sqlalchemy import Column, ForeignKey, Table
from app.common.db import Base

# For many-to-many relationship between Band and User

band_members = Table(
    "band_members",
    Base.metadata,
    Column("band_id", ForeignKey("bands.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

band_rehearsals = Table(
    "band_rehearsals",
    Base.metadata,
    Column("band_id", ForeignKey("bands.id", ondelete="CASCADE"), primary_key=True),
    Column("rehearsal_id", ForeignKey("rehearsals.id", ondelete="CASCADE"), primary_key=True),
)