from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.bands.models import Band
from app.common.db import get_db
from app.users.models import User
from app.bands.schemas import BandCreate

router = APIRouter(tags=["Bands"])

@router.get("/bands")
async def get_bands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Band))
    return result.scalars().all()

@router.get("/bands/{band_id}/members")
async def get_band_members(band_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        Band.__table__.select().where(Band.id == band_id)
    )
    band = result.scalar_one_or_none()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    await db.refresh(band)
    return band.members

@router.post("/bands/{band_id}/members/{user_id}")
async def add_band_member(band_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    band_result = await db.execute(
        Band.__table__.select().where(Band.id == band_id)
    )
    band = band_result.scalar_one_or_none()
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")

    user_result = await db.execute(
        User.__table__.select().where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    band.members.append(user)
    db.add(band)
    await db.commit()
    await db.refresh(user)
    return user

@router.post("/bands/create")
async def create_band(band: BandCreate, db: AsyncSession = Depends(get_db)):
    new_band = Band(
        name=band.name,
        creator_id=band.creator_id,
        is_active=True,
        is_approved=False,
    )
    db.add(new_band)
    await db.commit()
    await db.refresh(new_band)
    return new_band