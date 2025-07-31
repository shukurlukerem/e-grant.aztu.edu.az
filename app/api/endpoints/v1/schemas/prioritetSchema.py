from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrioritetBase(BaseModel):
    prioritet_name: str
    prioriet_code: int


class PrioritetCreate(BaseModel):
    prioritet_name: str
    prioritet_code: int


class PrioritetOut(PrioritetBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
