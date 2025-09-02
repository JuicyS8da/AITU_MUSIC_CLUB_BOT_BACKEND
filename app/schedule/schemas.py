from datetime import date, time

from pydantic import BaseModel, Field, validator

from app.bands.models import Band

class RehearsalBase(BaseModel):
    day: date = Field(..., description="The date of the rehearsal")
    time_start: time = Field(..., description="The start time of the rehearsal in HH:MM format")
    time_end: time = Field(..., description="The end time of the rehearsal in HH:MM format")

class RehearsalCreate(RehearsalBase):
    band_id: int

    @validator("time_start", "time_end", pre=True)
    def strip_seconds(cls, v):
        if isinstance(v, str):
            # Приводим строку "HH:MM" → datetime.time(HH, MM)
            hh, mm = map(int, v.split(":"))
            return time(hh, mm)
        return v

class RehearsalRead(RehearsalBase):
    id: int
    band_id: int

    class Config:
        orm_mode = True