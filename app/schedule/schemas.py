from datetime import date, time, datetime, timedelta

from pydantic import BaseModel, Field, validator, field_validator

from app.bands.models import Band

class RehearsalBase(BaseModel):
    day: date = Field(..., description="The date of the rehearsal")
    time_start: time = Field(..., description="The start time of the rehearsal in HH:MM format", examples=["18:30", "09:00"])
    time_end: time = Field(..., description="The end time of the rehearsal in HH:MM format", examples=["20:30", "11:00"])

class RehearsalCreate(RehearsalBase):
    band_id: int

    @validator("time_start", "time_end", pre=True)
    def strip_seconds(cls, v):
        if isinstance(v, str):
            # Приводим строку "HH:MM" → datetime.time(HH, MM)
            hh, mm = map(int, v.split(":"))
            return time(hh, mm)
        return v

    @field_validator("time_end")
    def check_duration(cls, v, info):
        start = info.data.get("time_start")
        if start and v:
            start_dt = datetime.combine(date.today(), start)
            end_dt = datetime.combine(date.today(), v)

            if end_dt <= start_dt:
                raise ValueError("Время окончания должно быть позже начала")

            duration = end_dt - start_dt
            if duration > timedelta(hours=2):
                raise ValueError("Репетиция не может быть дольше 2 часов")
        return v

class RehearsalRead(RehearsalBase):
    id: int
    band_id: int

    class Config:
        orm_mode = True

class RehearsalOut(BaseModel):
    id: int
    day: date
    time_start: time
    time_end: time
    band_id: int

    class Config:
        from_attributes = True