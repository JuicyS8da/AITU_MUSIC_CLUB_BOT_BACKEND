from datetime import date, time

from sqlalchemy import String, ForeignKey, Date, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.db import Base
from app.common.associations import band_members, band_rehearsals

class Rehearsal(Base):
    __tablename__ = "rehearsals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    day: Mapped[date] = mapped_column(Date, nullable=False)
    time_start: Mapped[time] = mapped_column(Time, nullable=False)
    time_end: Mapped[time] = mapped_column(Time, nullable=False)
    band_id: Mapped[int] = mapped_column(ForeignKey("bands.id", ondelete="CASCADE"))
    
    band: Mapped["Band"] = relationship("Band", back_populates="rehearsals")