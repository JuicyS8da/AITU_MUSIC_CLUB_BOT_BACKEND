from pydantic import BaseModel, Field

class BandCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    creator_id: int