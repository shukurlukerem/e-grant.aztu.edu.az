from pydantic import BaseModel
from typing import Optional

class SalaryCreateSchema(BaseModel):
    project_code: int
    fin_kod: str
    salary_per_month: int
    months: int

class SalaryUpdateSchema(BaseModel):
    fin_kod: str
    salary_per_month: Optional[int] = None
    months: Optional[int] = None

class SalaryResponseSchema(SalaryCreateSchema):
    id: int
    total_salary: int

    class Config:
        orm_mode = True