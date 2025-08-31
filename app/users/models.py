from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.associations import band_members
from app.common.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    bands: Mapped[list["Band"]] = relationship(
        "Band",
        secondary=band_members,
        back_populates="members",
    )