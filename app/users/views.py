from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, routing
from fastapi import HTTPException

from app.common.db import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserRead

router = routing.APIRouter()


@router.get("/users", response_model=list[UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users")
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    await db.commit()
    return new_user
