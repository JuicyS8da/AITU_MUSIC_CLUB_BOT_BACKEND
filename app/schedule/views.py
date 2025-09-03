from typing import List
from datetime import date, timedelta, datetime

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException

from app.common.db import get_async_session
from app.schedule.models import Rehearsal
from app.schedule.schemas import RehearsalCreate, RehearsalRead, RehearsalOut
from app.schedule.validators import validate_rehearsal

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.get("/rehearsals")
async def get_rehearsals(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Rehearsal))
    return result.scalars().all()

@router.get("/rehearsals/{rehearsal_id}", response_model=RehearsalRead)
async def get_rehearsal(rehearsal_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Rehearsal).where(Rehearsal.id == rehearsal_id))
    rehearsal = result.scalar_one_or_none()
    if rehearsal is None:
        raise HTTPException(status_code=404, detail="Rehearsal not found")
    return rehearsal

@router.post("/rehearsals/", response_model=RehearsalRead)
async def create_rehearsal(data: RehearsalCreate, session: AsyncSession = Depends(get_async_session)):
    # Проверяем лимит
    await validate_rehearsal(
        band_id=data.band_id,
        day=data.day,
        time_start=data.time_start,
        time_end=data.time_end,
        session=session
    )

    # Если всё ок → сохраняем
    rehearsal = Rehearsal(**data.dict())
    session.add(rehearsal)
    await session.commit()
    await session.refresh(rehearsal)
    return rehearsal

@router.get("/rehearsals/band/{band_id}", response_model=list[RehearsalRead])
async def get_rehearsals_by_band(band_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Rehearsal).where(Rehearsal.band_id == band_id))
    rehearsals = result.scalars().all()
    if not rehearsals:
        raise HTTPException(status_code=404, detail="No rehearsals found for this band")
    return rehearsals

@router.get("/rehearsals/day/{day}")
async def get_rehearsals_by_day(day: str, db: AsyncSession = Depends(get_async_session)):
    try:
        # поддержка формата ДД.ММ.ГГГГ
        parsed_day = datetime.strptime(day, "%d.%m.%Y").date()
    except ValueError:
        # если не получилось, пробуем ISO-формат (ГГГГ-ММ-ДД)
        try:
            parsed_day = datetime.strptime(day, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(400, "Неверный формат даты. Используйте ГГГГ-ММ-ДД или ДД.ММ.ГГГГ")

    query = select(Rehearsal).where(Rehearsal.day == parsed_day)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/rehearsals/week", response_model=List[RehearsalOut])
async def get_rehearsals_week(session: AsyncSession = Depends(get_async_session)):
    today = date.today()
    week_later = today + timedelta(days=7)
    query = select(Rehearsal).where(Rehearsal.day.between(today, week_later)).order_by(Rehearsal.day, Rehearsal.time_start)
    result = await session.execute(query)
    return result.scalars().all()