from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrioritetBase(BaseModel):
    priority_name: str
    project_code: int

class PrioritetCreate(PrioritetBase):
    pass

class PrioritetOut(PrioritetBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
