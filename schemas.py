from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class ClanIn(BaseModel):
    name: str
    region: Optional[str] = None

class ClanCreateResponse(BaseModel):
    id: UUID
    message: str

class ClanDeleteResponse(BaseModel):
    id: UUID
    message: str

class ClanOut(ClanIn):
    id: UUID
    created_at: datetime
# orm_mode is used to correctly map the fields for SQL Alchemy objects
    class Config:
        orm_mode = True
