from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy import select

from app.bands.models import Band
from app.common.db import get_async_session
from app.users.models import User
from app.bands.schemas import BandCreate

router = APIRouter(tags=["Bands"])

@router.get("/bands")
async def get_bands(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Band))
    return result.scalars().all()

@router.get("/bands/{band_id}/members")
async def get_band_members(band_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(
        select(Band).options(selectinload(Band.members)).where(Band.id == band_id)
    )
    band = result.scalar_one_or_none()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    await session.refresh(band)
    return band.members

@router.post("/bands/{band_id}/members/{user_id}")
async def add_band_member(band_id: int, user_id: int, session: AsyncSession = Depends(get_async_session)):
    band_result = await session.execute(
        select(Band).options(selectinload(Band.members)).where(Band.id == band_id)
    )
    band = band_result.scalar_one_or_none()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")

    user_result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    band.members.append(user)

    await session.commit()

    return {"message": f"User {user.id} added to band {band.id}"}

@router.post("/bands/create")
async def create_band(band: BandCreate, session: AsyncSession = Depends(get_async_session)):
    new_band = Band(
        name=band.name,
        creator_id=band.creator_id,
        is_active=True,
        is_approved=False,
    )
    session.add(new_band)
    await session.commit()
    await session.refresh(new_band)
    return new_band