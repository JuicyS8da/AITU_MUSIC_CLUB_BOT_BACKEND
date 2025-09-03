from datetime import datetime, date, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schedule.models import Rehearsal

MAX_WEEKLY_HOURS = 4
MAX_SINGLE_REHEARSAL_HOURS = 2

async def validate_rehearsal(band_id: int, day: date, time_start: datetime.time, time_end: datetime.time, session: AsyncSession):

    start_dt = datetime.combine(day, time_start)
    end_dt = datetime.combine(day, time_end)

    # Проверка: время окончания > начала
    if end_dt <= start_dt:
        raise HTTPException(400, "Время окончания должно быть позже начала")

    # Проверка: длительность ≤ 2 ч
    duration_hours = (end_dt - start_dt).seconds / 3600
    if duration_hours > MAX_SINGLE_REHEARSAL_HOURS:
        raise HTTPException(
            400,
            f"Репетиция не может быть дольше {MAX_SINGLE_REHEARSAL_HOURS} часов"
        )

    # Проверка лимита за неделю
    start_date = day
    end_date = day + timedelta(days=7)
    query = select(Rehearsal).where(
        Rehearsal.band_id == band_id,
        Rehearsal.day.between(start_date, end_date)
    )
    result = await session.execute(query)
    rehearsals = result.scalars().all()

    total_hours = sum(
        (datetime.combine(r.day, r.time_end) - datetime.combine(r.day, r.time_start)).seconds / 3600
        for r in rehearsals
    )

    if total_hours + duration_hours > MAX_WEEKLY_HOURS:
        raise HTTPException(
            400,
            f"У группы превышен лимит {MAX_WEEKLY_HOURS} часов на 7 дней"
        )

    # Проверка пересечений
    for r in rehearsals:
        r_start = datetime.combine(r.day, r.time_start)
        r_end = datetime.combine(r.day, r.time_end)

        if r.day == day and not (end_dt <= r_start or start_dt >= r_end):
            raise HTTPException(
                400,
                f"Репетиция пересекается с существующей: {r.time_start}-{r.time_end}"
            )
