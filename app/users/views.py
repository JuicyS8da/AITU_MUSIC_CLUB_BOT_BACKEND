from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, routing
from fastapi import HTTPException

from app.common.db import get_async_session
from app.users.models import User
from app.users.schemas import UserCreate, UserRead

router = routing.APIRouter(tags=["Users"])


@router.get("/users", response_model=list[UserRead])
async def get_users(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users")
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    new_user = User(**user_data.model_dump())
    session.add(new_user)
    await session.flush()
    await session.refresh(new_user)
    await session.commit()
    return new_user
