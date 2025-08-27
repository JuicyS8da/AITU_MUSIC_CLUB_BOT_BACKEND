from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    telegram_id: int
    username: str = Field(..., max_length=32)
    first_name: str = Field(..., max_length=64)
    last_name: str = Field(..., max_length=64)
    is_admin: bool = False
    is_active: bool = True

class UserRead(BaseModel):
    id: int
    telegram_id: int
    username: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True  # позволяет конвертировать ORM → Pydantic
