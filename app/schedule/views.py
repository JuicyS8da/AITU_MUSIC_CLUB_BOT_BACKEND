from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import Depends, HTTPException

from app.common.db import get_async_session
from app.schedule.models import Rehearsal
from app.schedule.schemas import RehearsalCreate, RehearsalRead

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
async def create_rehearsal(rehearsal_in: RehearsalCreate, session: AsyncSession = Depends(get_async_session),
):
    rehearsal = Rehearsal(day=rehearsal_in.day, time_start=rehearsal_in.time_start, time_end=rehearsal_in.time_end, band_id=rehearsal_in.band_id)
    session.add(rehearsal)
    await session.commit()
    await session.refresh(rehearsal)
    return rehearsal