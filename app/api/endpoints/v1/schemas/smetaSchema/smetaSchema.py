from pydantic import BaseModel
from typing import Optional

class SmetaBase(BaseModel):
    total_salary: Optional[int] = 0
    total_fee: Optional[int] = 0
    defense_fund: Optional[int] = 0
    total_equipment: Optional[int] = 0
    total_services: Optional[int] = 0
    total_rent: Optional[int] = 0
    other_expenses: Optional[int] = 0

class SmetaCreate(SmetaBase):
    project_code: int

class SmetaUpdate(SmetaBase):
    pass

class SmetaFieldUpdate(BaseModel):
    column: str
    value: int

class SmetaResponse(SmetaBase):
    project_code: int

class MainSmetaResponse(SmetaBase):
    total_main_amount: int
    max_amount_error: bool
